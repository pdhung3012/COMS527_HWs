import tensorflow.compat.v1 as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import Input
from tensorflow.keras.layers import MaxPool2D, Concatenate
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Layer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, LSTM, Conv1D, MaxPooling1D, Dropout, Activation, Conv2D, Reshape, \
    MaxPooling2D
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import Bidirectional
from tensorflow.keras import initializers, regularizers, constraints
from tqdm.notebook import tqdm
import math
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import KFold

from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
(train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()
uniqueLabel = set(test_labels.flatten())
uniqueLabel = sorted(uniqueLabel)
# Normalize pixel values to be between 0 and 1
train_images, test_images = train_images / 255.0, test_images / 255.0
test_labels_2 = test_labels.flatten()

arrActivationFunctions=['relu','tanh','sigmoid']
listTestAcc=[]
listConfigs=[]
listTotalContent=[]
for i1 in range(0,len(arrActivationFunctions)):
    for i2 in range(1,6):
        strFunc=arrActivationFunctions[i1]

        model = models.Sequential()
        model.add(Conv2D(32, (3, 3), activation=strFunc,kernel_initializer='he_normal', input_shape=(32, 32, 3)))
        model.add(MaxPooling2D((2, 2)))
        model.add(Conv2D(64, (3, 3), activation=strFunc,kernel_initializer='he_normal'))
        model.add(MaxPooling2D((2, 2)))
        model.add(Conv2D(64, (3, 3), activation=strFunc,kernel_initializer='he_normal'))
        model.summary()
        model.add(Flatten())
        model.add(Dense(64, activation=strFunc))
        model.add(Dense(10))

        model.compile(optimizer='adam',
                      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                      metrics=['accuracy'])

        history = model.fit(train_images, train_labels, epochs=i2,
                            validation_data=(test_images, test_labels))
        test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
        # print('test acc {}'.format(test_acc))
        # print(test_labels.shape)

        y_predict_number = model.predict(test_images)
        predict_labels=[]

        for index in range(len(y_predict_number)):
            listItem = y_predict_number[index].tolist()
            indexMax = listItem.index(max(listItem))
            predict_labels.append(indexMax)

        strConfig='{}-{}'.format(strFunc,i2)
        strConfusionMatrix=str(confusion_matrix(test_labels_2,predict_labels))
        strClassificationReport=str(classification_report(test_labels_2,predict_labels))
        listTestAcc.append(test_acc)
        listConfigs.append(strConfig)
        strElement='{}\nConfusion matrix: \n{}\nClassification report: \n{}\n\n\n'.format(test_acc,strConfusionMatrix,strClassificationReport)
        listTotalContent.append(strElement)
        # print('{}\n{}\n'.format(strConfusionMatrix,strClassificationReport))
listFinalLines=['List of accuracies: \n']
for i in range(0,len(listConfigs)):
    strItem='{}: {}\n'.format(listConfigs[i],listTestAcc[i])
    listFinalLines.append(strItem)

indexMax = listTestAcc.index(max(listTestAcc))
strBestConfig='Best config is {} at {}\n'.format(listConfigs[indexMax],listTestAcc[indexMax])
listFinalLines.append(strBestConfig)

f=open('HW6_Sum.txt','w')
f.write(''.join(listTotalContent))
f.write(''.join(listFinalLines))
f.close()