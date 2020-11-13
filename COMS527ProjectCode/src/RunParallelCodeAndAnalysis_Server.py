import os
import random

import pathlib
import time
import datetime
import timeit
from TestRunProcess import Command



fopInput='/home/hung/git/COMS527_data/Augment1/'
fopSerialTime='/home/hung/git/COMS527_data/Aug1-TimeAnalysis/'
fopOutputAnalysis='/home/hung/git/COMS527_data/Aug1-OutputAnalysis/'
fopTempAnalysis='/home/hung/git/COMS527_data/TempAnalysis/'


def createDirectory(path):
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)

createDirectory(fopSerialTime)
createDirectory(fopTempAnalysis)
createDirectory(fopOutputAnalysis)


# #1. create array of input.txt
# listInput=[]
# sizeArray=100
# for i in range(0,sizeArray):
#     listInput.append(str(random.randint(1,10)))
# strInput=' '.join(listInput).strip()
# fpInput=fopTempAnalysis+'inputTest.txt'
# file=open(fpInput,'w')
# file.write(strInput)
# file.close()

#2.
# define the path
currentDirectory = pathlib.Path(fopInput)
# define the pattern
currentPattern = "*.c"
listFiles=[]
for currentFile in currentDirectory.glob(currentPattern):
    listFiles.append(str(currentFile))

print('{}'.format(len(listFiles)))
# Command cmd;
timeOutSecond=2
for i in range(0,len(listFiles)):
    fileNameI=os.path.basename(listFiles[i]).replace('.c','')
    time_fileName='time-'+fileNameI+'.txt'
    output_fileName = 'output-'+fileNameI+'.txt'
    print('{} {} begin'.format((i + 1), fileNameI))
    try:
        strCommand1 = 'gcc  -fopenmp ' + listFiles[i] + ' -o ' + fopOutputAnalysis + fileNameI + '.o'
        strCommand2 = fopOutputAnalysis + fileNameI + ".o <" + fopTempAnalysis + "inputTest.txt >" + fopOutputAnalysis + output_fileName
        # os.system(strCommand1)
        command = Command(strCommand1)
        command.run(timeout=timeOutSecond)
        isFirstCmdOk=not command.isTimeOut
        # start_time = datetime.datetime.now()
        # end_time = datetime.datetime.now()
        # # os.system(strCommand2)
        # time_diff = (end_time - start_time)
        # execution_time = time_diff.total_seconds() * 1000
        # execution_time = timeit.timeit(stmt='os.system('+strCommand2+')', setup='import os;')
        isSecondCmdOk =False
        execution_time=0.0
        if(isFirstCmdOk):
            command = Command(strCommand2)
            command.run(timeout=timeOutSecond)
            isSecondCmdOk = not command.isTimeOut
            execution_time=command.timeExecution

        fTimeAnalysis = open(fopSerialTime + time_fileName, 'w')
        fTimeAnalysis.write('{}\n{}\n{}'.format(isFirstCmdOk,isSecondCmdOk,execution_time))
        fTimeAnalysis.close()
        print('{} {} ok'.format((i+1),fileNameI))
    except Exception as e:
        print('{} {} fail {}'.format((i + 1),fileNameI,str(e)))

    # if (i>=101):
    #     break
