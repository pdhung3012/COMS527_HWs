import os
import random

import pathlib
import time
import datetime
import timeit


fopInput='/home/hung/git/COMS527_data/PrutorCodes/'
fopTempAnalysis='/home/hung/git/COMS527_data/TempAnalysis/'

fopSerialTime='/home/hung/git/COMS527_data/SerialTimeAnalysis/'
fopOutputAnalysis='/home/hung/git/COMS527_data/OutputAnalysis/'

fopParallelTime='/home/hung/git/COMS527_data/Aug1-TimeAnalysis/'
fopParallelOutputAnalysis='/home/hung/git/COMS527_data/Aug1-OutputAnalysis/'

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

listSerialTime=[]
listSerialAnalysis=[]
listParallelTime=[]
listParallelAnalysis=[]
dictSerialTime={}
dictSerialAnalysis={}
dictParallelTime={}
dictParallelAnalysis={}

currentPattern = "*.txt"
listFiles=[]
currentDirectory = pathlib.Path(fopSerialTime)
for currentFile in currentDirectory.glob(currentPattern):
    strFilePath=str(currentFile)
    fileName=os.path.basename(strFilePath).replace('.txt','').replace('time-','')
    f=open(strFilePath,'r')
    strContent=f.read().strip()
    f.close()
    if(strContent.startswith('True\nTrue\n')):
        listSerialTime.append(fileName)
        num= float(strContent.split('\n')[2])
        dictSerialTime[fileName]=num

currentPattern = "*.txt"
listFiles=[]
currentDirectory = pathlib.Path(fopOutputAnalysis)
for currentFile in currentDirectory.glob(currentPattern):
    strFilePath=str(currentFile)
    fileName=os.path.basename(strFilePath).replace('.txt','').replace('output-','')
    f = open(strFilePath, 'r')
    strContent = f.read().strip()
    f.close()
    if ((strContent != '') and (not 'error' in strContent)):
        listSerialAnalysis.append(fileName)
        dictSerialAnalysis[fileName]=strContent


currentPattern = "*.txt"
listFiles=[]
currentDirectory = pathlib.Path(fopParallelTime)
for currentFile in currentDirectory.glob(currentPattern):
    strFilePath=str(currentFile)
    fileName=os.path.basename(strFilePath).replace('.txt','').replace('time-','')
    f = open(strFilePath, 'r')
    strContent = f.read().strip()
    f.close()
    if (strContent.startswith('True\nTrue\n')):
        listParallelTime.append(fileName)
        num = float(strContent.split('\n')[2])
        dictParallelTime[fileName] = num

currentPattern = "*.txt"
listFiles=[]
currentDirectory = pathlib.Path(fopParallelOutputAnalysis)
for currentFile in currentDirectory.glob(currentPattern):
    strFilePath=str(currentFile)
    fileName=os.path.basename(strFilePath).replace('.txt','').replace('output-','')
    f = open(strFilePath, 'r')
    strContent = f.read().strip()
    f.close()
    if ((strContent != '') and (not 'error' in strContent)):
        listParallelAnalysis.append(fileName)
        dictParallelAnalysis[fileName] = strContent

listNameIntersection=intersection(intersection(listParallelTime,listParallelAnalysis), intersection(listSerialTime,listSerialAnalysis))
strHead='Code,TimeSerial,TimeParallel,IsParallelBetterInTime,IsOutputConsistent'
lstTotal=[]
lstTotal.append(strHead)
numOfAbnormalInTime=0
numOfAbnormalInOutput=0
for i in range(0,len(listNameIntersection)):
    strName=listNameIntersection[i]
    isParallelBetterInTime=dictParallelTime[strName]>dictSerialTime[strName]
    isOutputConsistent=dictParallelAnalysis[strName]!=dictSerialAnalysis[strName]
    if not isParallelBetterInTime:
        numOfAbnormalInTime=numOfAbnormalInTime+1
    if not isOutputConsistent:
        numOfAbnormalInOutput=numOfAbnormalInOutput+1

    strLine='{},{},{},{},{},{}'.format(strName,dictSerialTime[strName],dictParallelTime[strName],isParallelBetterInTime,isOutputConsistent)
    lstTotal.append(strLine)

strContent='\n'.join(lstTotal)
f=open(fopTempAnalysis+'evaluation.csv','w')
f.write(strContent)
f.close()

percentAbTime=numOfAbnormalInTime*100.0/len(listNameIntersection)
percentAbOutput=numOfAbnormalInOutput*100.0/len(listNameIntersection)

strContent='Percent abnormal in time {} {} {}\nPercent abnormal in output {} {} {}\n'.format(numOfAbnormalInTime,len(listNameIntersection),percentAbTime,numOfAbnormalInOutput,len(listNameIntersection),percentAbOutput)
f=open(fopTempAnalysis+'summarization.txt','w')
f.write(strContent)
f.close()








