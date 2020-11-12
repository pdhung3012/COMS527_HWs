import os
import random

import pathlib
import time
import datetime
import timeit
from TestRunProcess import Command



fopInput='/Users/hungphan/git/COMS527/PrutorCodes/'
fopSerialTime='/Users/hungphan/git/COMS527/SerialTimeAnalysis/'
fopOutputAnalysis='/Users/hungphan/git/COMS527/OutputAnalysis/'
fopTempAnalysis='/Users/hungphan/git/COMS527/TempAnalysis/'


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
    try:



    except Exception as e:
        print('{} {} fail {}'.format((i + 1),fileNameI,str(e)))

    if (i>=1001):
        break
