from glob import glob
from PIL import Image
import numpy as np
from math import log
from math import exp
from matplotlib import pyplot as plt
import csv
from sklearn.decomposition import PCA
from libsvm.python.svmutil import *
from libsvm.tools.grid import *
import os
def read( datafile ):           #read demo data
    temp=[]
    file=open(datafile,'r')
    r=csv.reader(file)
    for row in r:
        temp.append(list(map(float,row)))
    return np.array(temp)

def write( savefile ,lable ,feature ):      #rewrite libsvm data type 
    lable=lable.flatten().tolist()
    temp=[]
    tp=[]
    for row in range(len(feature)):
        for j in range(len(feature[0])):
            temp.append(str(j+1)+':'+str(feature[row,j]))
        tp.append(temp)
        temp=[]
        
    with open(savefile,'w',newline='') as f:
        for row in range(len(tp)):
            f.write(str(lable[row]))
            f.write(' ')
            for column in range(len(tp[0])):
                f.write(tp[row][column])
                if column != len(tp[0])-1:
                    f.write(' ')
                elif row!=len(tp)-1:
                    f.write('\n')

#data name list       
xTrain=read( "data/X_train.csv")
tTrain=read( "data/T_train.csv")
xTest=read( "data/X_test.csv")
tTest=read( "data/T_test.csv")
write( 'train.txt', tTrain, xTrain )
write( 'test.txt', tTest, xTest )



'''
#reduce dimention for the figure 
pca=PCA(n_components=2)
pca.fit(xTrain)
xTrainTrans=pca.transform(xTrain)
xTestTrans=pca.transform(xTest)
'''

'''

#optimize the parameter using grid.py for c-svm
os.system('python grid.py -log2c -3,3,1 -log2g -3,3,1 -t 0 -png s0t0.png train.txt')

os.system('python grid.py -log2c -3,3,1 -log2g -3,3,1 -t 1 -d 2 -png s0t1d2.png train.txt')

os.system('python grid.py -log2c -3,3,1 -log2g -3,3,1 -t 1 -d 3 -png s0t1d3.png train.txt')

os.system('python grid.py -log2c -3,3,1 -log2g -3,3,1 -t 1 -d 4 -png s0t1d4.png train.txt')

os.system('python grid.py -log2c -3,3,1 -log2g -3,3,1 -t 2 -png s0t2.png train.txt')


'''
'''
#svm training
y, x = svm_read_problem('train.txt')
yt, xt = svm_read_problem('test.txt')
model=svm_train(y,x,'-s 1 -t 1')
svm_predict(yt,xt,model)
'''

'''
#plot the scatter figure
X=xTrainTrans
plt.plot(xTrainTrans[:1000,0],xTrainTrans[:1000,1],'o',color='b')
plt.plot(xTrainTrans[1000:2000,0],xTrainTrans[1000:2000,1],'o',color='c')
plt.plot(xTrainTrans[2000:3000,0],xTrainTrans[2000:3000,1],'o',color='g')
plt.plot(xTrainTrans[3000:4000,0],xTrainTrans[3000:4000,1],'o',color='m')
plt.plot(xTrainTrans[4000:5000,0],xTrainTrans[4000:5000,1],'o',color='r')
plt.show()
'''
