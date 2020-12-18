import os
import random

import pathlib
import time
import datetime
import timeit


fopInput='/Users/hungphan/Desktop/importantDocuments/Utilities-2020/'
fpOutput='/Users/hungphan/Desktop/importantDocuments/util_fileAndDate.txt'


def createDirectory(path):
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)

currentDirectory = pathlib.Path(fopInput)
# define the pattern
currentPattern = "*.JPG"
listFiles=[]
for currentFile in sorted(currentDirectory.glob(currentPattern)):
    listFiles.append(str(currentFile))

lstStr=[]
for i in range(0,len(listFiles)):
    fileNameI = os.path.basename(listFiles[i]).replace('.c', '')
    lstStr.append(fileNameI)
sorted(lstStr)

fp=open(fpOutput,'w')
fp.write('\n'.join(lstStr))
fp.close()