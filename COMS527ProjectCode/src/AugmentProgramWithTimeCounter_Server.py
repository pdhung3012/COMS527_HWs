import os
import random

import pathlib
import time
import datetime
import timeit
from TestRunProcess import Command
import clang.cindex
from TestClangProgram import *


fopInput='/home/hung/git/COMS527_data/PrutorCodes/'
fopAugmentedParallel='/home/hung/git/COMS527_data/TimeCounterPrograms-Parallel/'
fopAugmentedSerial='/home/hung/git/COMS527_data/TimeCounterPrograms-Serial/'

# fopSerialTime='/Users/hungphan/git/COMS527/SerialTimeAnalysis/'
# fopOutputAnalysis='/Users/hungphan/git/COMS527/OutputAnalysis/'
# fopTempAnalysis='/Users/hungphan/git/COMS527/TempAnalysis/'


def createDirectory(path):
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)

createDirectory(fopAugmentedParallel)
createDirectory(fopAugmentedSerial)


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
clang.cindex.Config.set_library_file('/home/hung/anaconda3/pkgs/libclang-8.0.1-hc9558a2_2/lib/libclang.so')

strPragmaForTemplate='#pragma omp parallel for'
strSetThreadFunction='omp_set_num_threads(16);'
strIncludeOMP='#include<omp.h>\n#include <time.h>'
strBeginCounterCmds='\tclock_t start_t = clock();'
strEndCounterCmds='\tclock_t stop_t = clock();\n\tdouble elapsed_t = (double)(stop_t - start_t) * 1000.0 / CLOCKS_PER_SEC;\n\tprintf(\"\\nTime elapsed in ms: %f\", elapsed_t);'

timeOutSecond=2
for i in range(0,len(listFiles)):
    fileNameI=os.path.basename(listFiles[i]).replace('.c','')
    fpAugmentedFileParallel= fopAugmentedParallel + fileNameI + '.c'
    fpAugmentedFileSerial = fopAugmentedSerial + fileNameI + '.c'
    try:
        index = clang.cindex.Index.create()
        tu = index.parse(listFiles[i])
        root = tu.cursor
        index = 0
        indexOfForLoop = 0
        walker = Walker(listFiles[i])
        walker.walkInForLoopAndKeepTrackReturnStatement(root, index, indexOfForLoop)
        listForLoops=walker.listForLoops
        print('Handle {} {}'.format((i+1),listFiles[i]))
        if (len(listForLoops)>0):
            setLineFor = set()
            dictLines={}
            for j in range(0, len(listForLoops)):
                setLineFor.add(listForLoops[j].lineNumber)
                dictLines[listForLoops[j].lineNumber]=listForLoops[j]
            f1=open(listFiles[i],'r')
            strF1=f1.read()
            f1.close()
            arrF1=strF1.split('\n')

            lstNewParallelStr=[]
            lstNewParallelStr.append(strIncludeOMP)
            lstNewSerialStr=[]
            lstNewSerialStr.append(strIncludeOMP)
            isAddFunction=False

            lineToAddBeginExecution=-1
            lineJ=walker.lineBeginOfMainFunction
            strTemp=arrF1[lineJ].strip()
            if strTemp.startswith('{'):
                lineToAddBeginExecution=lineJ+1
            else:
                lineToAddBeginExecution=walker.lineBeginOfMainFunction

            for j in range(0,len(arrF1)):
                if (j+1) == (lineToAddBeginExecution+1):
                    lstNewParallelStr.append(strBeginCounterCmds)
                    lstNewSerialStr.append(strBeginCounterCmds)
                elif (j+1) == (walker.lineEndOfMainFunction):
                    lstNewParallelStr.append(strEndCounterCmds)
                    lstNewSerialStr.append(strEndCounterCmds)
                elif (j+1) in setLineFor:
                    if((not isAddFunction) and (dictLines[(j+1)].funcName=='main')):
                        lstNewParallelStr.append(strSetThreadFunction)
                        isAddFunction=True
                    lstNewParallelStr.append(strPragmaForTemplate)
                lstNewParallelStr.append(arrF1[j])
                lstNewSerialStr.append(arrF1[j])

            strAugmentedC='\n'.join(lstNewParallelStr)
            f1=open(fpAugmentedFileParallel, 'w')
            f1.write(strAugmentedC)
            f1.close()
            strAugmentedC = '\n'.join(lstNewSerialStr)
            f1 = open(fpAugmentedFileSerial, 'w')
            f1.write(strAugmentedC)
            f1.close()







    except Exception as e:
        print('{} {} fail {}'.format((i + 1),fileNameI,str(e)))

    # if (i>=1001):
    #     break
