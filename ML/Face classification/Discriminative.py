import csv 
from glob import glob
import math
from PIL import Image
import numpy as np 
import matplotlib.pyplot as plt

def CPA(tm):
    #making Covarian matrix 
    cov = np.cov(tm)
    value, vector = np.linalg.eig(cov)  #eigenvalue eigenvector
    maximum = np.array([vector[:,0]])
    smax = np.array([vector[:,1]])    #second maximun
    v = np.vstack((maximum,smax))  #combine two vector
    return v

def outputFile(ans):
    pof = open( 'DemoTarget.csv' , 'w', newline='') ;
    wri = csv.writer(pof) ;
    for row in ans  :
        wri.writerow(row) ;
    pof.close()
    
def seperateD(data):
    #sperate data into validation and learning data
    test=[] 
    test.append(data[900:1000,:])
    test.append(data[1900:2000,:])
    test.append(data[2900:3000,:])
    test = np.array(test) #(3,100,900)
    test = test.flatten()
    test = np.reshape(test,(300,900))
    test = test.T
    data = np.delete(data,list(range(900,1000)),0)
    data = np.delete(data,list(range(1800,1900)),0)
    data = np.delete(data,list(range(2700,2800)),0)
    return test,data

def yk( w, phi):
    w = w.reshape((3,3))
    ak = np.dot( w, phi.T)    #(3,2700)
    #Compute yk
    ak = ak.T   #(2700,3)
    shape = phi.shape
    for row in range(shape[0]) :
        ma = np.amax(ak[row])
        total = sum( math.exp(a-ma) for a in ak[row] )
        for col in range(3) :
            ak[row][col] = math.exp(ak[row][col]-ma)/total
    return ak
def deltaE(phi,y,t):
    deltaE = np.zeros((9,1))
    for data in range(2700) :
        for dim in range(3):
            for i in range(3):
                deltaE[i+3*dim][0]= deltaE[i+3*dim][0]+(y[data][dim]-t[data][dim])*phi[data][i]
    return deltaE

def Hessian( phi,y,t ):
    h = np.zeros((3,3,3,3))
    for data in range(2700) :
        temp = phi[data]
        temp = temp.reshape(1,3)
        temp = np.dot(temp.T,temp)
        for k in range(3):
            for j in range(3):
                if k==j :
                    scalar = y[data][k]*(1-y[data][j])
                    h[k][j] = h[k][j] + scalar*temp
                else :
                    scalar = -y[data][k]*y[data][j]
                    h[k][j] = h[k][j] + scalar*temp 
    h = h.swapaxes(1, 2).reshape((9,9))
    return h
    
def newton( phi , w, t, test , miner , minw ):
    #unstoppable
    y = yk(w,phi)
    dE = deltaE(phi,y,t)  #(9,1) col-class row-phi.
    h = Hessian(phi,y,t)  #(9,9)
    try:
        inh = np.linalg.inv(h)
    except np.linalg.linalg.LinAlgError as err:
        return minw
    nw = w - np.dot( inh,dE )
    e = error(nw,test)
    if e < miner  :
        miner = e
        minw = nw
    if np.array_equal(nw,w) or e==0 or e>miner :
        return minw
    else :
       return newton( phi, nw, t, test, miner, minw )

def answer(y) :
    ans = [] 
    for row in y:
        temp = [0,0,0]
        i = np.argmax(row)
        temp[i] = 1 ;
        ans.append(temp)
    return ans
        
def error( w, test ):
    ans = yk( w, test )
    ans = answer(ans)   #(300,3)
    error = 0 ;
    for i in range(300):
        if i<100 :
            if ans[i][0]!=1 :
                error = error + 1
        elif i<200 :
            if ans[i][1]!=1 :
                error = error + 1
        elif i<300 :
            if ans[i][2]!=1 :
                error = error + 1
    print(error)
    return error
    
def mean(data):
    #row dimension
    mu=[]
    for row in data :
        m = sum(a for a in row) / 2700
        mu.append(m)
    return mu

def subtractMean( data, mu ):
    shape = data.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            data[i][j] = data[i][j] - mu[i]
    return data

def decisionRigion( nw ):
    # tw (3,2)
    x1= np.array(range(2306,2345,1))
    x2= np.array(range(680,2305,5))
    x3= np.array(range(2305,4600,5))
    x12 = (x1*(nw[4]-nw[1])+nw[3]-nw[0])/(nw[2]-nw[5])
    x13 = (x2*(nw[7]-nw[1])+nw[6]-nw[0])/(nw[2]-nw[8])
    x23 = (x3*(nw[7]-nw[4])+nw[6]-nw[3])/(nw[5]-nw[8])
    return x1,x2,x3,x12,x13,x23

def show_Graph( matrix, test, nw):
    #red for class 1
    plt.plot(matrix[0][:900],matrix[1][:900],color='red',markersize=1,ls='',marker='o',label='class1')
    plt.plot(test[0][:100],test[1][:100],color='red',ls='',markersize=1,marker='o',label='class1')
    #blue for class 2
    plt.plot(matrix[0][900:1800],matrix[1][900:1800],color='blue',markersize=1,ls='',marker='o',label='class2')
    plt.plot(test[0][100:200],test[1][100:200],color='blue',markersize=1,ls='',marker='o',label='class2')
    #green for class 3
    plt.plot(matrix[0][1800:2700],matrix[1][1800:2700],markersize=1,ls='',color='green',marker='o',label='class3')
    plt.plot(test[0][200:300],test[1][200:300],color='green',markersize=1,ls='',marker='o',label='class3')
    #draw decision region
    x1,x2,x3,x12,x13,x23 = decisionRigion(nw)
    plt.plot(x1,x12,color='red',markersize=1,marker='o')
    plt.plot(x2,x13,color='green',markersize=1,marker='o')
    plt.plot(x3,x23,color='blue',markersize=1,marker='o')
    plt.xlim([500,4700])
    plt.ylim([-500,3200])
    plt.show()
    
#Main function  
files = glob('Data_Train/**/*.bmp', recursive = True )
matrix = np.array( [ np.array(Image.open(f)).flatten() for f in files ] )   #(3000,900)
file = glob("Demo/*.bmp")
demo = np.array( [ np.array(Image.open(f)).flatten() for f in file ] ).T
#choose 100 pics from each class
test,matrix = seperateD(matrix)
#Transpose learning matrix data
matrix = matrix.T #(900,2700)
#target matrix
t = []
for i in range(2700):
    if i<900 :
        t.append([1,0,0])
    elif i<1800:
        t.append([0,1,0])
    else :
        t.append([0,0,1])
t = np.array(t)
mu = mean(matrix)
matrix = subtractMean(matrix,mu)
test = subtractMean(test,mu)
demo = subtractMean(demo,mu)
# projecting
v = CPA(matrix)   # projective data(2,900)
matrix = np.dot(v,matrix)   #new learning data
test = np.dot(v,test)     #new testing data
demo = v.dot(demo).T
nt = np.insert(test.T,0,1,axis=1)
demo = np.insert(demo,0,1,axis=1)
#Newton-Taphson method
phi = matrix.T  #(2700,2)
phi = np.insert(phi,0,1,axis=1)  #(2700,3)
w =[]
w.append([1e-19,1e-19,1e-19,1e-19,1e-19,1e-19,1e-19,1e-19,1e-19])
w = np.array(w)
w = w.T

e = error(w,nt) 
nw = newton(phi,w,t,nt,e,w)   #new w
#Answering demo
ans = answer( yk(nw, demo) )

show_Graph(matrix,test,nw)

#output File
outputFile(ans)

