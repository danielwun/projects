import tensorflow as tf
from glob import glob
import numpy as np
import cv2

#face detector
faceCascade = cv2.CascadeClassifier("data/haarcascades/haarcascade_frontalface_default.xml")
eyeCascade = cv2.CascadeClassifier("data/haarcascades/haarcascade_eye.xml")

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

def max_pool_2x2(x):
    #ksize pool size [數據量,高,寬,channel]
    #strides為步數 [數據量,影像高,影像寬,channel]
    # padding=SAME 卷積完與原本同維度
    return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME', name="pooling")

def norm(x, lsize=4):
    return tf.nn.lrn(x, lsize, bias=1.0, alpha=0.001 / 9.0, beta=0.75)

def datalist():
    #選擇讀檔路徑
    path = [[]]*8
    path[0] = glob("child/male/*.jpg")
    path[0] = sorted(path[0], key = lambda x:int(x[11:-4]) )
    
    path[1] = glob("young/male/*.jpg")
    path[1] = sorted(path[1], key = lambda x:int(x[11:-4]) )
    
    path[2] = glob("adult/male/*.jpg")
    path[2] = sorted(path[2], key = lambda x:int(x[11:-4]) )
    
    path[3] = glob("elder/male/*.jpg")
    path[3] = sorted(path[3], key = lambda x:int(x[11:-4]) )
    
    path[4] = glob("child/female/*.jpg")
    path[4] = sorted(path[4], key = lambda x:int(x[13:-4]) )
    
    path[5] = glob("young/female/*.jpg")
    path[5] = sorted(path[5], key = lambda x:int(x[13:-4]) )
    
    path[6] = glob("adult/female/*.jpg")
    path[6] = sorted(path[6], key = lambda x:int(x[13:-4]) )
    
    path[7] = glob("elder/female/*.jpg")
    path[7] = sorted(path[7], key = lambda x:int(x[13:-4]) )
    
    return path

def face_detect(path):
    #以openCV做臉部偵測並縮放到28*28
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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

    
def data_process(path_list):
    #將只取出臉的圖片轉成TensorFlow接受的形式
    val_num = 30
    data = []
    val = []
    num = np.zeros(8)

    for index,row in enumerate(path_list):
        tmp = 0
        for column in row:
            '''
            resize = face_detect(column)
            if type(resize) == int:
                continue
            '''
            image = cv2.imread(column)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            #resize = cv2.resize(gray, (data_h,data_w), interpolation=cv2.INTER_AREA)
            
            
            if tmp<val_num:
                val.append(gray/255)
            else:
                data.append(gray/255)
            tmp += 1
        num[index] = tmp-val_num
        
    data = np.array(data, dtype = "float32").reshape((int(sum(num)), n_input))
    val = np.array(val, dtype = "float32").reshape((val_num*8, n_input))
    
    data_label = []
    data_kof1 = []
    val_label = []
    val_kof1 = []
    for i in range(8):
        data_label.extend(np.ones(int(num[i]))*i)
        val_label.extend(np.ones(val_num)*i)
    for i in range(val_num*8):
        tmp = np.zeros(8)
        tmp[int(val_label[i])] = 1
        val_kof1.append(tmp)
    for i in range(int(sum(num))):
        tmp = np.zeros(8)
        tmp[int(data_label[i])] = 1
        data_kof1.append(tmp)
    #以one-of-k編碼輸出標籤
    val_kof1 = np.array(val_kof1).reshape((8*val_num,8))
    data_kof1 = np.array(data_kof1).reshape((int(sum(num)),8))

    return data, data_kof1, val, val_kof1

def mini_batch(data, label , number):
    #以mini batch做back propagation
    batch_x = []
    batch_y = []
    for i in range(number):
        random_num = np.random.randint(0,len(data))
        batch_x.append(data[random_num])
        batch_y.append(label[random_num])
    batch_x = np.array(batch_x).reshape((number, data.shape[1]))
    batch_y = np.array(batch_y).reshape((number, 8))
    
    return [batch_x, batch_y]
def net(data, weights, biases, dropout):
    # reshape到[圖片數,高,寬,channel]
    x_image = tf.reshape(data, [-1,data_h,data_w,1])

    #conv layer 1
    h_conv1 = tf.nn.relu(conv2d(x_image, weights['wc1']) + biases['bc1'])
    #max pooling
    h_pool1 = max_pool_2x2(h_conv1)
    h_pool1 = tf.nn.dropout(h_pool1, keep_prob)

    #conv layer 2
    h_conv2 = tf.nn.relu(conv2d(h_pool1, weights['wc2']) + biases['bc2'])
    h_pool2 = max_pool_2x2(h_conv2)
    h_pool2 = tf.nn.dropout(h_pool2, keep_prob)

    #fully connected layer
    h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, weights['wfc1']) + biases['bfc1'])
    #apply dropout
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    #output layer
    out=tf.nn.softmax(tf.matmul(h_fc1_drop, weights['out']) + biases['out'])
    return out

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


#find the path of data
path = datalist()
#data process  data = [N,high*width] lable using 1 of k
data, data_label, test, test_label = data_process(path)


sess = tf.InteractiveSession()
#consturct the model
y_conv = net(x, weights, biases, keep_prob)

#define loss and optimizer
cross_entropy = -tf.reduce_sum(y_*tf.log(y_conv))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

#evaluate model
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


loss=[]
acc=[]
step=[]
test_acc=[]

#initializing the variables
sess.run( tf.global_variables_initializer() )
#save the model 
saver = tf.train.Saver()
for i in range(100000):
    batch = mini_batch(data, data_label ,20)

    if i%100 == 0:
        train_accuracy = accuracy.eval(feed_dict={
            x:batch[0], y_: batch[1], keep_prob: 1.0})
        train_cross_entropy = cross_entropy.eval(feed_dict={
            x:batch[0], y_: batch[1], keep_prob: 1.0})
        loss.append(train_cross_entropy)
        acc.append(train_accuracy)
        
        step.append(i)
        if i!=0 and max(test_acc) < accuracy.eval(feed_dict={
    x: test, y_: test_label, keep_prob: 1.0}):
            saver.save(sess,"./model.ckpt")
        test_acc.append(accuracy.eval(feed_dict={
    x: test, y_: test_label, keep_prob: 1.0}))
        print("step %d, loss %g, training accuracy %g"%(i, train_cross_entropy, train_accuracy))
    train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.8})


print("test accuracy %g"%accuracy.eval(feed_dict={
    x: test, y_: test_label, keep_prob: 1.0}))



#pred = tf.argmax(y_conv,1)
#print(pred.eval(feed_dict={x:test, keep_prob: 1.0}))
