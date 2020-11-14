import os
import random

import pathlib
import time
import datetime
import timeit


fopInput='/home/hung/git/COMS527_data/PrutorCodes/'
fopTempAnalysis='/home/hung/git/COMS527_data/TempAnalysis/'

fopSerialTime='/home/hung/git/COMS527_data/SerialTimeAnalysis_1000/'
fopOutputAnalysis='/home/hung/git/COMS527_data/OutputAnalysis_1000/'

fopParallelTime='/home/hung/git/COMS527_data/Aug1-TimeAnalysis_1000/'
fopParallelOutputAnalysis='/home/hung/git/COMS527_data/Aug1-OutputAnalysis_1000/'

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

# currentPattern = "*.txt"
# listFiles=[]
# currentDirectory = pathlib.Path(fopSerialTime)
# for currentFile in currentDirectory.glob(currentPattern):
#     strFilePath=str(currentFile)
#     listFiles.append(strFilePath)
#
# for strFilePath in listFiles:
#     fileName=os.path.basename(strFilePath).replace('.txt','').replace('time-','')
#     f=open(strFilePath,'r')
#     strContent=f.read().strip()
#     f.close()
#     # print(strContent)
#     print('serial time {}'.format(fileName))
#     if(strContent.startswith('True\nTrue\n')):
#         listSerialTime.append(fileName)
#         num= float(strContent.split('\n')[2])
#         dictSerialTime[fileName]=num
#
# currentPattern = "*.txt"
# listFiles=[]
# currentDirectory = pathlib.Path(fopOutputAnalysis)
# for currentFile in currentDirectory.glob(currentPattern):
#     strFilePath=str(currentFile)
#     listFiles.append(strFilePath)
#
# for strFilePath in listFiles:
#     fileName=os.path.basename(strFilePath).replace('.txt','').replace('output-','')
#     try:
#         f = open(strFilePath, 'r', encoding="utf-8")
#         strContent = f.read().strip()
#         f.close()
#     except Exception as e:
#         strContent=''
#     # print('aaa {}'.format(strContent))
#
#     print('serial o {}'.format(fileName))
#     if ((strContent != '') and (not 'error' in strContent)):
#
#         listSerialAnalysis.append(fileName)
#         dictSerialAnalysis[fileName]=strContent


currentPattern = "*.txt"
listFiles=[]
listNameIntersection=[]
currentDirectory = pathlib.Path(fopParallelTime)
for currentFile in currentDirectory.glob(currentPattern):
    strFilePath=str(currentFile)
    listFiles.append(strFilePath)
# print('Parallel size {}'.format(len(listFiles)))
for i in range(0,len(listFiles)):
    strFilePath=listFiles[i]

    isTimeSerialOK=False
    isOutputSerialOK = False
    isTimeParallelOK = False
    isOutputParallelOK = False

    fileName=os.path.basename(strFilePath).replace('.txt','').replace('time-','')
    strContentTimeParallel=''
    try:
        f = open(strFilePath, 'r', encoding="latin-1")
        strContentTimeParallel = f.read().strip()
        f.close()
    except Exception as e:
        strContentTimeParallel = ''
    # print('go here {}'.format(strContent))
    # print('parallel time {}'.format(fileName))
    if (strContentTimeParallel.startswith('True\nTrue\n')):
        # listParallelTime.append(fileName)
        isTimeParallelOK=True
        num = float(strContentTimeParallel.split('\n')[2])
        dictParallelTime[fileName] = num

    fpOutputParallel=fopParallelOutputAnalysis+'output-'+fileName+'.txt'
    print(fpOutputParallel)
    strContentOutputParallel = ''
    try:
        f = open(fpOutputParallel, 'r', encoding="latin-1")
        strContentOutputParallel = f.read().strip()
        f.close()
    except Exception as e:
        # print(str(e))
        strContentOutputParallel = ''
    # print('parallel o {}'.format(fileName))
    if ((strContentOutputParallel != '') and (not 'error' in strContentOutputParallel)):
        # listParallelAnalysis.append(fileName)
        # print('go here')
        isOutputParallelOK=True
        dictParallelAnalysis[fileName] = strContentOutputParallel

    fpTimeSerial = fopSerialTime + 'time-' + fileName + '.txt'
    strContentTimeSerial = ''
    try:
        f = open(fpTimeSerial, 'r', encoding="latin-1")
        strContentTimeSerial = f.read().strip()
        f.close()
    except Exception as e:
        strContentTimeSerial = ''
    if(strContentTimeSerial.startswith('True\nTrue\n')):
        # listSerialTime.append(fileName)
        isTimeSerialOK=True
        num= float(strContentTimeSerial.split('\n')[2])
        dictSerialTime[fileName]=num

    fpOutputSerial = fopOutputAnalysis + 'output-' + fileName + '.txt'
    strContentOutputSerial = ''
    try:
        f = open(fpOutputSerial, 'r', encoding="latin-1")
        strContentOutputSerial = f.read().strip()
        f.close()
    except Exception as e:
        strContentOutputSerial=''
    if ((strContentOutputSerial != '') and (not 'error' in strContentOutputSerial)):
        isOutputSerialOK=True
        listSerialAnalysis.append(fileName)
        dictSerialAnalysis[fileName]=strContentOutputSerial

    print('{} {} {} {}'.format(isTimeParallelOK,isOutputParallelOK,isTimeSerialOK,isOutputSerialOK))
    if(isTimeParallelOK and isOutputParallelOK and isTimeSerialOK and isOutputSerialOK):
        listNameIntersection.append(fileName)
        print('{} file {} is OK'.format((i+1),fileName))
    else:
        print('{} file {} is missing'.format((i + 1), fileName))

strHead='Code,TimeSerial,TimeParallel,IsParallelBetterInTime,IsOutputConsistent,IsAllConsistent'
lstTotal=[]
lstTotal.append(strHead)
numOfAbnormalInTime=0
numOfAbnormalInOutput=0
numOfAbnormalInTotal=0
totalMillisecondSerial=0
totalMillisecondParallel=0
for i in range(0,len(listNameIntersection)):
    strName=listNameIntersection[i]
    isParallelBetterInTime=dictParallelTime[strName]<dictSerialTime[strName]
    isOutputConsistent=dictParallelAnalysis[strName]!=dictSerialAnalysis[strName]
    isAllConsistent=isParallelBetterInTime and isOutputConsistent
    if not isParallelBetterInTime:
        numOfAbnormalInTime=numOfAbnormalInTime+1
    if not isOutputConsistent:
        numOfAbnormalInOutput=numOfAbnormalInOutput+1
    if not isAllConsistent:
        numOfAbnormalInTotal=numOfAbnormalInTotal+1
    timeSerial=dictSerialTime[strName]
    timeParallel=dictParallelTime[strName]
    totalMillisecondSerial=totalMillisecondSerial+timeSerial
    totalMillisecondParallel = totalMillisecondParallel + timeParallel
    strLine='{},{},{},{},{},{}'.format(strName,timeSerial,timeParallel,isParallelBetterInTime,isOutputConsistent,isAllConsistent)
    lstTotal.append(strLine)

strContent='\n'.join(lstTotal)
f=open(fopTempAnalysis+'evaluation.csv','w')
f.write(strContent)
f.close()

percentAbTime=numOfAbnormalInTime*100.0/len(listNameIntersection)
percentAbOutput=numOfAbnormalInOutput*100.0/len(listNameIntersection)
percentAbTotal=numOfAbnormalInTotal*100.0/len(listNameIntersection)

strContent='Percent abnormal in time {} {} {}\nPercent abnormal in output {} {} {}\nPercent abnormal in total {} {} {}\nTotal milliseconds in Serial: {}\nTotal milliseconds in Parallel: {}\n'.format(numOfAbnormalInTime,len(listNameIntersection),percentAbTime,numOfAbnormalInOutput,len(listNameIntersection),percentAbOutput,len(listNameIntersection),numOfAbnormalInTotal,percentAbTotal,totalMillisecondSerial,totalMillisecondParallel)
f=open(fopTempAnalysis+'summarization.txt','w')
f.write(strContent)
f.close()








