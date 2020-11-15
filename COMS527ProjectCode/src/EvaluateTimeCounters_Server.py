import os
import random

import pathlib
import time
import datetime
import timeit


fopInput='/home/hung/git/COMS527_data/PrutorCodes/'
fopTempAnalysis='/home/hung/git/COMS527_data/TempAnalysis/'
# fopSerialTime='/home/hung/git/COMS527_data/TimeAnalysis_all/'
fopOutputAnalysis='/home/hung/git/COMS527_data/OutputAnalysis_all/'
# fopParallelTime='/home/hung/git/COMS527_data/Aug1-TimeAnalysis_all/'
fopParallelOutputAnalysis='/home/hung/git/COMS527_data/Aug1-OutputAnalysis_all/'

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
def extractPrintOutputAndTime(strContent):
    arrContent=strContent.split('\n')
    strPrint=''
    strTime=''
    if(len(arrContent)>=2):
        strTime=arrContent[len(arrContent)-1]
        l = list(arrContent)
        l.pop()
        strPrint='\n'.join(l)
    return strPrint,strTime

listSerialTime=[]
listSerialAnalysis=[]
listParallelTime=[]
listParallelAnalysis=[]
dictSerialTime={}
# dictSerialAnalysis={}
dictParallelTime={}
# dictParallelAnalysis={}
dictOutputSame={}

currentPattern = "*.txt"
listFiles=[]
listNameIntersection=[]
currentDirectory = pathlib.Path(fopParallelOutputAnalysis)
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

    fileName=os.path.basename(strFilePath).replace('.txt','').replace('output-','')
    strContentParallel=''
    strContentTimeParallel=''
    strContentOutputParallel=''

    try:
        f = open(strFilePath, 'r', encoding="latin-1")
        strContentParallel = f.read().strip()
        strContentOutputParallel,strContentTimeParallel=extractPrintOutputAndTime(strContentParallel)
        f.close()
    except Exception as e:
        strContentParallel = ''
    if (strContentTimeParallel.startswith('Time elapsed in ms: ')):
        # listParallelTime.append(fileName)
        isTimeParallelOK=True
        strTime=strContentTimeParallel.replace('Time elapsed in ms: ','').strip()
        num = float(strTime)
        dictParallelTime[fileName] = num
    if ((strContentOutputParallel != '') and (not 'error' in strContentOutputParallel)):
        isOutputParallelOK=True


    fpOutputSerial = fopOutputAnalysis + 'output-' + fileName + '.txt'
    strContentSerial = ''
    strContentTimeSerial=''
    strContentOutputSerial=''
    try:
        f = open(fpOutputSerial, 'r', encoding="latin-1")
        strContentSerial = f.read().strip()
        f.close()

    except Exception as e:
        strContentSerial=''
    strContentOutputSerial,strContentTimeSerial=extractPrintOutputAndTime(strContentSerial)
    if (strContentTimeSerial.startswith('Time elapsed in ms: ')):
        # listSerialTime.append(fileName)
        isTimeSerialOK = True
        strTime = strContentTimeSerial.replace('Time elapsed in ms: ', '').strip()
        num = float(strTime)
        dictSerialTime[fileName] = num

    if ((strContentOutputSerial != '') and (not 'error' in strContentOutputSerial)):
        isOutputSerialOK=True
        listSerialAnalysis.append(fileName)
        # dictSerialAnalysis[fileName]=strContentOutputSerial

    # print('{} {} {} {}'.format(isTimeParallelOK,isOutputParallelOK,isTimeSerialOK,isOutputSerialOK))
    if(isTimeParallelOK and isOutputParallelOK and isTimeSerialOK and isOutputSerialOK):
        listNameIntersection.append(fileName)

        if strContentOutputSerial == strContentOutputParallel:
            dictOutputSame[fileName]=True
        else:
            dictOutputSame[fileName]=False

        print('{} file {} is OK'.format((i+1),fileName))
    else:
        print('{} file {} is missing'.format((i + 1), fileName))
    if i == 1000:
        break

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
    isOutputConsistent=dictOutputSame[strName]
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








