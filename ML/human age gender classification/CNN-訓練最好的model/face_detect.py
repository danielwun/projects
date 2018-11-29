from glob import glob
import cv2
import numpy as np
path = glob('data/young/male/*.jpg')


#openCV detector
faceCascade = cv2.CascadeClassifier("detector/haarcascades/haarcascade_frontalface_default.xml")
eyeCascade = cv2.CascadeClassifier("detector/haarcascades/haarcascade_eye.xml")
for index,file in enumerate(path):
    #指定存檔路徑
    save_path = 'CNN/young/male/'+index+'.jpg'
    image = cv2.imread(file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faceArray = faceCascade.detectMultiScale(gray, 1.1, 5)
    size=0
    tmp=[]
    #作臉部辨識以並縮放到28*28
    #若同時辨識到多張臉 則取辨識出的範圍最大的當作臉
    if type(faceArray)!=tuple:
        if len(faceArray)!=1:
            '''
            for (x ,y ,w ,h) in faceArray:
                if w*h>size and x+w <= gray.shape[1] and y+h<=gray.shape[0]:
                    size= w*h
                    tmp=[x,y,w,h]
            faceArray=np.array(tmp).reshape((1,4))
            '''
            faceArray = sorted(faceArray, key = lambda x:x[2]*x[3])
            
        for (x, y, w, h) in faceArray:
            #cv2.rectangle(image, (x, y), (x+w, y+h), (182, 89, 255), 2)
            roi_gray = gray[y:y+h, x:x+w]
            
            eyeArray = eyeCascade.detectMultiScale(roi_gray)

            if type(eyeArray) != tuple :
                res=cv2.resize(roi_gray,(28,28),interpolation=cv2.INTER_AREA)
                cv2.imwrite(save_path,res)
                break


            




