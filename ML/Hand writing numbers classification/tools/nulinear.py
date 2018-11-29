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
def main():
    # read as libsvm format
    label, learning = svm_read_problem('learningfile')
    tlabel , tlearning = svm_read_problem('testfile')
    accuracy = []
    n = []
    for nu in range(1,99,5):
        os.system('svm-train -s 1 -t 0 -n '+str(float(nu/100))+' learningfile learningfile.model')    
        os.system('svm-predict testfile learningfile.model result.out')    
        label = readLabel('result.out')
        acc = Accuracy(tlabel, label)
        n.append(nu)
        accuracy.append(acc)
        print(nu,' ',acc)
    plt.plot( n, accuracy, color='red',ls='',marker='o',)
    plt.xlabel('n')
    plt.ylabel('accuracy(%)')
    plt.savefig('nulinear.png')
    plt.show()
    
    
if __name__ == "__main__":
    main()
