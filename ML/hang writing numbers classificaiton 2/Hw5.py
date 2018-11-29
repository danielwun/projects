import csv 
import glob
import math
from PIL import Image
import numpy as np 
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from libsvm.python.svmutil import *
from sklearn import tree
import pydotplus

def outputFile( wzx, time ):
    pof = open( 'parameter'+str(time)+'.csv' , 'w', newline='') ;
    wri = csv.writer(pof) ;
    for row in wzx  :
        wri.writerow(row) ;
    pof.close()
    
def readFile( fname ):
    data = []
    f = open( fname , 'r') ;    #location file
    for row in csv.reader(f) :
        data.append(row)
    f.close();
    return data

def pca( data1 , data2 ):
    pc = PCA(n_components=2)
    pc.fit(data1)
    data1 = pc.transform(data1)
    data2 = pc.transform(data2)
    return data1, data2

def neural_Learning( x, wzx, wyz, z, y, t) :
    for i in range(x.shape[0]) :
        z = forward_Propagation_Z( x[i], wzx, z)
        y = forward_Propagation_Y( z, wyz, y)
        wyz = back_Propagation_Z( wyz, y, t[i], z)
        wzx = back_Propagation_X( wzx, wyz, y, t[i], x[i], z )
    return wzx, wyz

def forward_Propagation_Z( inpu, w, outpu ):
    size = w.shape[0]
    for i in range(size) :
        outpu[i] = np.dot( w[i].T, inpu)
        #print(outpu[i][0])
        if outpu[i]>= 45 :
            outpu[i] = 1
        elif outpu[i]<-500 :
            outpu[i] = 0
        else:
            outpu[i] = 1/( 1+ math.exp(-1*outpu[i]) )
    return outpu

def forward_Propagation_Y( inpu, w, outpu ):
    size = w.shape[0]
    total = 0
    maximum = 0
    for i in range(size) :
        outpu[i] = np.dot( w[i].T, inpu)
        if outpu[i] > maximum :
            maximum = outpu[i]
    for i in range(size):
        outpu[i] = math.exp(outpu[i]-maximum)
        total = total + outpu[i]
    outpu = outpu/total
    return outpu

def back_Propagation_Z( w, y, t, z):
    for i in range( w.shape[0]):
        for j in range( w.shape[1] ) :
            w[i][j] = w[i][j]-0.001*(y[i]-t[i])*z[j]
    return w

def back_Propagation_X( wzx, wyz, y, t, x, z ):
    for j in range( wzx.shape[0] ):
        if z[j]==0 or z[j]==1:
            h_aj = 0
        else:
            e_a = 1/z[j]-1   # exp(-a)
            h_aj = e_a*(z[j])*(z[j])  # h'(aj)
        temp = 0
        for k in range(y.shape[0]):
            temp = temp + wyz[k][j]*( y[k]-t[k] )
        temp = temp * h_aj
        for i in range( wzx.shape[1] ):
            wzx[j][i] = wzx[j][i] - 0.001*temp*x[i]
            #print(wzx[j][i])
        #input()    
    return wzx

def dimReduction(inpu, w , outpu) :   
    for i in range(w.shape[0]) :
        outpu[i] = np.dot( w[i].T, inpu)
        if outpu[i]>= 45 :
            outpu[i] = 1
        elif outpu[i]<-500 :
            outpu[i] = 0
        else:
            outpu[i] = 1/( 1+ math.exp(-1*outpu[i]) )
    return outpu

def resultList(t):
    result = []
    for i in range(t.shape[0]):
        temp = [0,0,0,0,0]
        temp[t[i][0]-1] = 1
        result.append(temp)
    return np.array(result)

def showGraph( decisiontree, num ) :
    dot_data = tree.export_graphviz(decisiontree, out_file=None,
                         class_names=['1','2','3','4','5'],  
                         filled=True, rounded=True,  
                         special_characters=True)  
    graph = pydotplus.graph_from_dot_data(dot_data)
    #Image( graph.create_png(), filename='test'+str(num)+'.png')
    graph.write_png("test"+'7'+'-'+str(num)+".png")
    
def bagging( x_learn, t_learn, fraction):
    a = np.random.randint( 5000, size=(int(5000*fraction)) )
    x = []
    y = [] 
    for i in range(int(5000*fraction)) :
        x.append( x_learn[a[i]] )
        y.append( t_learn[a[i]] )
    return x, y

def decisionTree(fraction, nd, t_learn, nd_test ):        
    forest = []
    T = [] 
    for i in range(100):
        x, y = bagging( nd, t_learn, fraction)    
        dt = tree.DecisionTreeClassifier( min_samples_leaf=1000 )   #decision tree
        forest.append( dt.fit( x, y ) )
        if i%49==0 :
            T.append( dt.fit( x,y ) ) 
            #showGraph( dt.fit( x, y), i/49 )
    result = np.zeros(1) ;
    for t in forest :
        result = np.add( result, t.predict_proba( nd_test ))
    result = result / 100 
    return result

def accuracy( result, t_test ) :
    size = result.shape[0]
    error = 0 
    for i in range( size ) :
        if (np.argmax(result[i])+1 ) !=  t_test[i] :
            error = error + 1 
    return float(error/size)

def readParameter(filename):
    wzx = []
    with open( filename,'r') as f:
        for row in csv.reader(f):
            wzx.append( np.array(row, dtype=float) )
    return np.array(wzx)

def main():

    x_learn = np.array(readFile("data\X_train.csv"), dtype=float)
    t_learn = np.array(readFile("data\T_train.csv"), dtype=int)
    x_test = np.array(readFile("data\X_test.csv"), dtype=float)
    t_test = np.array(readFile("data\T_test.csv"), dtype=int)

    t = resultList(t_learn)
    hlayer = 5+1   #hidden layer
    x = np.insert( x_learn, 784, 1, axis=1)
    x_test = np.insert( x_test, 784, 1, axis=1)
    wzx = readParameter('parameter.csv')
    print('dimensional reduction parameter find!')
    
    nd = []     #data after dimension reduction  
    nd_test = [] 
    for datanum in range(x_learn.shape[0]):
        nd.append(dimReduction( x[datanum], wzx,  np.ones(hlayer-1)))
    for i in range( x_test.shape[0] ) :
        nd_test.append(dimReduction( x_test[i], wzx,  np.ones(hlayer-1)))
    print('dimensional reduction done!')

    fraction = 0.5  # fraction of samples
    result = decisionTree( fraction, nd, t_learn, nd_test)
    print(' error rate= ',accuracy(result, t_test ))
        
if __name__ == "__main__":
    main()
