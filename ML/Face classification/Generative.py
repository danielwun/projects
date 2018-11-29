import csv 
import glob
import math
from PIL import Image
import numpy as np 
import matplotlib.pyplot as plt

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
    test = np.array(test)
    test = test.flatten()
    test = np.reshape(test,(300,900))
    test = test.T
    data = np.delete(data,list(range(900,1000)),0)
    data = np.delete(data,list(range(1800,1900)),0)
    data = np.delete(data,list(range(2700,2800)),0)
    return test,data

def Error(ans) :
    num = 0 ;
    error = 0 ;
    for data in ans :
        if num<100 :
            if data[0] != 1:
                error = error+1 ;
        elif num<200:
            if data[1] != 1:
                error = error+1 ;
        else :
            if data[2] != 1:
                error = error+1 ;
        num = num+1 ;
    return error
def coefficient(nd):
    #return the coefficients of ak(x)
    #Generative Classification
    pc1 = 1/3   #probability of c1 
    pc2 = 1/3   #probability of c2
    pc3 = 1/3   #probability of c3

    mu1 = [sum(nd[0][:900])/900,sum(nd[1][:900])/900]    #mean of c1
    mu2 = [sum(nd[0][900:1800])/900,sum(nd[1][900:1800])/900]   #mean of c2
    mu3 = [sum(nd[0][1800:2700])/900,sum(nd[1][1800:2700])/900]    #mean of c3

    #new covariance 
    s1 = [ [sum((nd[0][i]-mu1[0])*(nd[0][i]-mu1[0]) for i in range(900))/2700 , sum( (nd[0][i]-mu1[0])*(nd[1][i]-mu1[1]) for i in range(900))/2700] ]
    s1.append( [ sum((nd[1][i]-mu1[1])*(nd[0][i]-mu1[0]) for i in range(900))/2700,sum((nd[1][i]-mu1[1])*(nd[1][i]-mu1[1]) for i in range(900))/2700])
    s2 = [ [sum((nd[0][i]-mu2[0])*(nd[0][i]-mu2[0]) for i in range(900,1800))/2700 , sum( (nd[0][i]-mu2[0])*(nd[1][i]-mu2[1]) for i in range(900,1800))/2700] ]
    s2.append( [ sum((nd[1][i]-mu2[1])*(nd[0][i]-mu2[0]) for i in range(900,1800))/2700,sum((nd[1][i]-mu2[1])*(nd[1][i]-mu2[1]) for i in range(900,1800))/2700])
    s3 = [ [sum((nd[0][i]-mu3[0])*(nd[0][i]-mu3[0]) for i in range(1800,2700))/2700 , sum( (nd[0][i]-mu3[0])*(nd[1][i]-mu3[1]) for i in range(1800,2700))/2700] ]
    s3.append( [ sum((nd[1][i]-mu3[1])*(nd[0][i]-mu3[0]) for i in range(1800,2700))/2700,sum((nd[1][i]-mu3[1])*(nd[1][i]-mu3[1]) for i in range(1800,2700))/2700])
    #new covariance
    nc=[]
    for i in range(2):
        nc.append([])
        for j in range(2):
            nc[i].append(float(s1[i][j])+float(s2[i][j])+float(s3[i][j]))
    del s1,s2,s3
    mu=[]
    mu.append(mu1)
    mu.append(mu2)
    mu.append(mu3)
    del mu2,mu3,mu1 ;
    icov = np.linalg.inv(nc)
    tmu = np.transpose(mu)
    w = np.dot(icov,tmu)
    omega = -0.5*np.dot(np.dot(mu,icov),tmu)+math.log(1/3)
    omega = [omega[0][0],omega[1][1],omega[2][2]]
    tw = np.transpose(w) 
    return tw,omega

def ak( tw, omega, x):
    #return a classification array
    a=[] 
    for test in x:
        maxi = 0 #maximum index
        temp=[]
        for i in range(3) :
            temp.append(np.dot(tw[i],test)+omega[i] )
        a.append(temp) ;
    return a

def yk( y ):
    ans = [] 
    for row in y:
        temp = [0,0,0]
        i = np.argmax(row)
        temp[i] = 1 ;
        ans.append(temp)
    return ans
        
def CPA(tm):
    #making Covarian matrix 
    cov = np.cov(tm)
    value, vector = np.linalg.eig(cov)  #eigenvalue eigenvector
    maximum = np.array([vector[:,0]])
    smax = np.array([vector[:,1]])    #second maximun
    v = np.vstack((maximum,smax))  #combine two vector
    return v
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
def decisionRigion( tw, omega ):
    # tw (3,2)
    x1= np.array(range(500,2685,5))
    x2= np.array(range(500,2685,5))
    x3= np.array(range(2685,4700,5))
    x12 = (x1*(tw[1][0]-tw[0][0])+omega[1]-omega[0])/(tw[0][1]-tw[1][1])
    x13 = (x2*(tw[2][0]-tw[0][0])+omega[2]-omega[0])/(tw[0][1]-tw[2][1])
    x23 = (x3*(tw[2][0]-tw[1][0])+omega[2]-omega[1])/(tw[1][1]-tw[2][1])
    return x1,x2,x3,x12,x13,x23

def show_Graph(matrix,test,tw,omega):
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
    x1,x2,x3,x12,x13,x23 = decisionRigion(tw,omega)
    plt.plot(x1,x12,color='red',markersize=1,marker='o')
    plt.plot(x2,x13,color='green',markersize=1,marker='o')
    plt.plot(x3,x23,color='blue',markersize=1,marker='o')
    plt.xlim([500,4700])
    plt.ylim([-500,3300])
    plt.show()


#Main function
files = glob.glob('Data_Train/**/*.bmp', recursive = True )
matrix = np.array( [ np.array(Image.open(f)).flatten() for f in files ] )
file = glob.glob("Demo/*.bmp")
demo = np.array( [ np.array(Image.open(f)).flatten() for f in file ] ).T
#choose 100 pics from each class
test,matrix = seperateD(matrix)
#Transpose learning matrix data
matrix = matrix.T #(900,2700)
mu = mean(matrix)
matrix = subtractMean(matrix,mu)
test = subtractMean(test,mu)
demo = subtractMean(demo,mu)
#projective vector
v = CPA(matrix)   # new data(2,900)
nd = np.dot(v,matrix)   #new learning data
nt = np.dot(v,test)     #new testing data
demo = v.dot(demo).T

tw,omega = coefficient(nd)

#making ak(x) function
nt = nt.T
ans = yk(ak(tw,omega,nt))
#Error function
print(Error(ans),'/',300)

outans = yk(ak(tw,omega,demo)) #output answer
#print output file
#outputFile(ans)
show_Graph(nd,nt.T,tw,omega)
