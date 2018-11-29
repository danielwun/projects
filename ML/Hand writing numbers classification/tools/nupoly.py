import csv 
import glob
import math
from PIL import Image
import numpy as np 
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from libsvm.python.svmutil import *
from libsvm.python.svm import *
import os
def readLabel(file):
    t=[]
    f = open( file, 'r' )
    for row in csv.reader(f) :
        for a in row :
            t.append(a)
    f.close()
    return t

def Accuracy( t, x):
    length = len(t)
    match = 0
    for i in range(length):
        if int(t[i]) == int(x[i]) :
            match = match + 1
    return float(match/length)
def outputFile( filename, nu, accuracy):
    accuracy = np.array(accuracy)
    maxi = np.argmax(accuracy)
    pof = open( filename , 'w', newline='')
    pof.write( 'n= ',str(nu[maxi])+' log2g= '+str(-8+2*maxi%8) +' accuracy ='+str(accuracy[maxi]) ) 
    pof.close()
def output(nu, acc, filename):
    X,Y = np.meshgrid( np.linspace(1,101,num=20,endpoint=False), np.linspace(-6,8,7,endpoint=False))
    plt.xlabel('n')
    plt.ylabel('log2g')
    Z = np.zeros((7,20))
    for i in range(20):
        for j in range(7):
            Z[j][i] = acc[i]
    plt.figure()
    CS = plt.contour(X, Y, Z, 5, linewidth=.5)
    plt.clabel(CS, inline=1, fontsize=5)
    plt.title(filename)
    plt.savefig( filename+'.png' )
    outputFile( filename+'.txt', nu, acc )
def main():
    # read as libsvm format
    label, learning = svm_read_problem('learningfile')
    tlabel , tlearning = svm_read_problem('testfile')
    accuracy = []
    n = []
    for d in range(2,3):
        for nu in range(1,99,5):
            #for g in range(-6,8,2) :
            os.system('svm-train -s 1 -t 1 -n '+str(float(nu/100))+' -g 1 -d '+str(d)+' learningfile nupoly2.model')    
            os.system('svm-predict testfile nupoly2.model result'+str(d)+'.out')    
            label = readLabel('result'+str(d)+'.out')
            acc = Accuracy(tlabel, label)
            n.append(nu)
            accuracy.append(acc)
            print('d= ',d,'nu= ',nu ,' ',acc)
        filename = 'nupoly'+str(d)    
        output(n,accuracy,filename)
        
if __name__ == "__main__":
    main()
