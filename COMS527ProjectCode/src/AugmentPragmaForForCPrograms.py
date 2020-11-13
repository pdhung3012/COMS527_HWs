import os
import random

import pathlib
import time
import datetime
import timeit
from TestRunProcess import Command
import clang.cindex
from TestClangProgram import *


fopInput='/Users/hungphan/git/COMS527/PrutorCodes/'
fopAugmented='/Users/hungphan/git/COMS527/Augment1/'

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

createDirectory(fopAugmented)


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

strPragmaForTemplate='#pragma omp parallel for'
strSetThreadFunction='omp_set_num_threads(16);'
strIncludeOMP='#include<omp.h>'
timeOutSecond=2
for i in range(0,len(listFiles)):
    fileNameI=os.path.basename(listFiles[i]).replace('.c','')
    fpAugmentedFile=fopAugmented+fileNameI+'.c'
    try:
        index = clang.cindex.Index.create()
        tu = index.parse(listFiles[i])
        root = tu.cursor
        index = 0
        indexOfForLoop = 0
        walker = Walker(listFiles[i])
        walker.walkInForLoop(root, index, indexOfForLoop)
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

            lstNewStr=[]
            lstNewStr.append(strIncludeOMP)
            isAddFunction=False
            for j in range(0,len(arrF1)):
                if (j+1) in setLineFor:
                    if((not isAddFunction) and (dictLines[(j+1)].funcName=='main')):
                        lstNewStr.append(strSetThreadFunction)
                        isAddFunction=True
                    lstNewStr.append(strPragmaForTemplate)
                lstNewStr.append(arrF1[j])

            strAugmentedC='\n'.join(lstNewStr)
            f1=open(fpAugmentedFile,'w')
            f1.write(strAugmentedC)
            f1.close()







    except Exception as e:
        print('{} {} fail {}'.format((i + 1),fileNameI,str(e)))

    if (i>=1001):
        break
