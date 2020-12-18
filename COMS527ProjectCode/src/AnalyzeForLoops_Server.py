import os
import random

import pathlib
import time
import datetime
import timeit
# from TestRunProcess import Command
import clang.cindex
from ForItemAnalysisWalker import *
import traceback

import math
def convertToNumber (s):
    return int.from_bytes(s.encode(), 'little')

def convertFromNumber (n):
    return n.to_bytes(math.ceil(n.bit_length() / 8), 'little').decode()

fopInput='/home/hung/git/COMS527_data/PrutorCodes/'
fopAnalyzeResult= '/home/hung/git/COMS527_data/AnalyzeForLoops/'
fopDetails= '/home/hung/git/COMS527_data/AnalyzeForLoops/details/'

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

createDirectory(fopAnalyzeResult)
createDirectory(fopDetails)

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
# clang.cindex.Config.set_library_file('/home/hung/anaconda3/pkgs/libclang-8.0.1-hc9558a2_2/lib/libclang.so')

dictAppearance={}
dictListFiles={}

for i in range(0,len(listFiles)):
    fileNameI=os.path.basename(listFiles[i]).replace('.c','')
    fpAugmentedFileParallel= fopAnalyzeResult + fileNameI + '.c'
    try:
        index = clang.cindex.Index.create()
        tu = index.parse(listFiles[i])
        root = tu.cursor

        f1 = open(listFiles[i], 'r')
        strF1 = f1.read()
        f1.close()
        arrF1 = strF1.split('\n')

        index = 0
        indexOfForLoop = 0
        walker = ForItemAnalysisWalker(listFiles[i])
        walker.walkInForLoop(root, index)
        listForLoops=walker.listForLoopsAfterVisits
        for j in range(0,len(listForLoops)):
            itemFor=listForLoops[j]
            lstForContent=[]
            for itt in itemFor.setOfLines:
                lstForContent.append(arrF1[itt-1])

            strContentItem='\n'.join(lstForContent).strip()
            strContentItem=strContentItem.replace('\t',' ').replace('\n',' ').strip()
            idContent=convertToNumber(strContentItem)
            # idContent = strContentItem
            # print(idContent)
            if not idContent in dictAppearance:
                # print('{}'.format(idContent))
                dictAppearance[str(idContent)]=1
                listItem=[]
                listItem.append(fileNameI)
                dictListFiles[str(idContent)]=listItem
            else:
                dictAppearance[str(idContent)] = dictAppearance[str(idContent)]+1
                dictListFiles[str(idContent)].append(fileNameI)
        print('Handle {} {}'.format((i+1),listFiles[i]))
    except Exception as e:
        print('{} {} fail {}'.format((i + 1),fileNameI,str(e)))
        traceback.print_exc()
    # if (i>=1001):
    #     break

sorted(dictAppearance.items(), key=lambda x: x[1], reverse=True)

fpOut=fopAnalyzeResult+'analysisFor.txt'
f=open(fpOut,'w')
print('count: {}'.format(len(dictAppearance)))
index=0
for key in dictAppearance.keys():
    index=index+1
    val=convertFromNumber(int(key))
    f.write('{}\t{}\n'.format(index,dictAppearance[key]))
    fpDeIt=fopDetails+str(index)+'.txt'
    f2=open(fpDeIt,'w')
    f2.write(val+'\n')
    f2.write(','.join(dictListFiles[key])+'\n')
    f2.close()
f.close()

