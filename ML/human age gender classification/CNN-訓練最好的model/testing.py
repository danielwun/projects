import tensorflow as tf
from glob import glob
import numpy as np
import cv2
import csv

#input data resize to
data_h = 28
data_w = 28

#Network Parameters
n_input = data_h*data_w
n_classes = 8
dropout = 1 

#tf Graph input
x = tf.placeholder(tf.float32, [None, n_input])
y_ = tf.placeholder(tf.float32, [None, 8])
keep_prob = tf.placeholder(tf.float32)


def weight_var(shape):
    #初始化權重
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial,name="W")

def bias_var(shape):
    #初始化常數項
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial, name="bias")

def conv2d(x,W):
    #定義卷積層
    # x,W為四維參數 
    #strides為步數 [數據量,影像高,影像寬,channel]
    # padding=SAME 卷積完與原本同維度
    return tf.nn.conv2d(x, W, strides=[1,1,1,1], padding="SAME", name="conv2D")

def conv2d(x,W):
    #定義卷積層
    # x,W為四維參數 
    #strides為步數 [數據量,影像高,影像寬,channel]
    # padding=SAME 卷積完與原本同維度
    return tf.nn.conv2d(x, W, strides=[1,1,1,1], padding="SAME", name="conv2D")

def max_pool_2x2(x):
    #ksize pool size [數據量,高,寬,channel]
    #strides為步數 [數據量,影像高,影像寬,channel]
    # padding=SAME 卷積完與原本同維度
    return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME', name="pooling")

def net(data, weights, biases, dropout):
    # reshape到[圖片數,高,寬,channel]
    x_image = tf.reshape(data, [-1,data_h,data_w,1])

    #conv layer 1
    h_conv1 = tf.nn.relu(conv2d(x_image, weights['wc1']) + biases['bc1'])
    #max pooling
    h_pool1 = max_pool_2x2(h_conv1)


    #conv layer 2
    h_conv2 = tf.nn.relu(conv2d(h_pool1, weights['wc2']) + biases['bc2'])
    h_pool2 = max_pool_2x2(h_conv2)


    #fully connected layer
    h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, weights['wfc1']) + biases['bfc1'])
    #apply dropout
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    #output layer
    out=tf.nn.softmax(tf.matmul(h_fc1_drop, weights['out']) + biases['out'])
    return out

def cascade():
    face_cascade = []
    face_cascade.append(cv2.CascadeClassifier('detector/haarcascades/haarcascade_profileface.xml'))
    face_cascade.append(cv2.CascadeClassifier('detector/haarcascades/haarcascade_frontalface_default.xml'))
    face_cascade.append(cv2.CascadeClassifier('detector/haarcascades/haarcascade_frontalface_alt.xml'))
    face_cascade.append(cv2.CascadeClassifier('detector/haarcascades/haarcascade_frontalface_alt2.xml'))
    face_cascade.append(cv2.CascadeClassifier('detector/haarcascades/haarcascade_frontalface_alt_tree.xml'))
    eye_cascade = []
    eye_cascade.append(cv2.CascadeClassifier('detector/haarcascades/haarcascade_eye_tree_eyeglasses.xml'))
    return face_cascade, eye_cascade

def findFace( face_cascade, eye_cascade, image):
    hh = image.shape[0]  #image hight
    ww = image.shape[1]  #image width
    faces = np.ones((0,))
    reyes = np.ones((0,))
    for face_detection in face_cascade :
        faces = np.array(face_detection.detectMultiScale( image, 1.1, 5))
        find = 0 
        if faces.size != 0 :
            for (x,y,w,h) in faces:
                #roi_gray = gray[y:y+h, x:x+w]
                roi_color = image[y:y+h, x:x+w]
                for eye_detection in eye_cascade:
                    eyes = np.array( eye_detection.detectMultiScale(roi_color) )
                    if eyes.size != 0 :
                        for (ex,ey,ew,eh) in eyes:
                            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)                
                            
                            # y direction extention
                            if ey+int(0.5*eh) > h-ey-int(0.5*eh) :
                                
                                y1 =  int(y)
                                y2 =  y + int(ey+0.5*eh)*2
                                if y2 > hh :
                                    y2 = hh
                            else :
                                
                                y1 = y+h - int((h-ey-0.5*eh)*2)
                                if y1 < 0 :
                                    y1 = 0
                                y2 = y + int(1.1*h)
                                if y2 > hh :
                                    y2 = hh
                                    
                            # x direction extention
                            if ex+int(0.5*ew) > w-ex-int(0.5*ew):
                                
                                x1 = int(x)
                                x2 = x+ 2*(ex+int(0.5*ew))
                                if x2 > ww :
                                    x2 = ww 
                            else :
                                
                                x1 = x+w-2*(w-ex-int(0.5*ew))
                                if x1< 0 :
                                    x1= 0
                                x2 = x + int(w*1.1)
                                if x2 > ww:
                                    x2=ww 
                            return 1, image[ y1:y2, x1:x2]
    return 0, image

def face_detect(path):
    #face detector
    faceCascade = cv2.CascadeClassifier("detector/haarcascades/haarcascade_frontalface_default.xml")
    eyeCascade = cv2.CascadeClassifier("detector/haarcascades/haarcascade_eye.xml")
    
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    '''
    gray = pow(gray/255,1/2)*255
    gray = gray.astype(dtype=np.uint8)
    '''
    faceArray = faceCascade.detectMultiScale(gray, 1.1, 5)
    
    size=0
    tmp=[]  
    if type(faceArray)!=tuple:
        if len(faceArray)!=1:
            faceArray = sorted(faceArray, key = lambda x:x[2]*x[3])
            
        for (x, y, w, h) in faceArray:
            #cv2.rectangle(image, (x, y), (x+w, y+h), (182, 89, 255), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = image[y:y+h, x:x+w]
            
            eyeArray = eyeCascade.detectMultiScale(roi_gray)

            if type(eyeArray) != tuple :
                res=cv2.resize(roi_gray,(28,28),interpolation=cv2.INTER_AREA)
                return res
    return 0

def data_process(path):
    data_num = int(len(path))
    data=[]
    face_cascade,eye_cascade = cascade()
    
    for file in path:
        image = face_detect(file)
        if type(image) == int:

            image = cv2.imread(file)
            find, image = findFace( face_cascade, eye_cascade, image)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.resize(gray,(28,28),interpolation=cv2.INTER_AREA)
        data.append(image/255)
        '''
        image = cv2.imread(file)
        #find, image = findFace( face_cascade, eye_cascade, image)
         
        res = cv2.resize(gray,(28,28),interpolation=cv2.INTER_AREA)
        data.append(res/255)
        '''
        
    data = np.array(data, dtype = "float32").reshape(data_num,28*28)
    
    return data
    

weights ={
    'wc1' : weight_var([5, 5, 1, 32]),
    'wc2' : weight_var([3, 3, 32, 64]),
    'wfc1': weight_var([7*7*64, 1024]),
    'out' : weight_var([1024, 8])
    }


biases = {
    'bc1' : bias_var([32]),
    'bc2' : bias_var([64]),
    'bfc1': bias_var([1024]),
    'out' : bias_var([8])
    }

testing_list = glob("testing/*.jpg")
testing_list = sorted(testing_list, key = lambda x:int(x[8:-4]))

data = data_process(testing_list)

sess = tf.InteractiveSession()
y_conv = net(x, weights, biases, keep_prob)

sess.run( tf.global_variables_initializer() )

#導入model
saver = tf.train.Saver()
saver.restore(sess, "./model/model.ckpt")
print("Model restored.")

pred = tf.argmax(y_conv,1)

ans=[]
for i in range(len(data)):
  ans.append([testing_list[i][8:-4], pred.eval(feed_dict={x:data, keep_prob: 1.0})[i]])

#預測輸出至target.csv
with open('target.csv', 'w', newline='') as out:
    write = csv.writer(out)
    write.writerows(ans)
