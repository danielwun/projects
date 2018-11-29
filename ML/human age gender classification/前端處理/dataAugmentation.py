import numpy as np
import glob
import cv2
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from scipy import ndimage
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
                            print('ey ',ey,' another ',h-ey-eh)
                            # y direction extention
                            if ey+int(0.5*eh) > h-ey-int(0.5*eh) :
                                print('y1')
                                y1 =  int(y)
                                y2 =  y + int(ey+0.5*eh)*2
                                if y2 > hh :
                                    y2 = hh
                            else :
                                print('y2')
                                y1 = y+h - int((h-ey-0.5*eh)*2)
                                if y1 < 0 :
                                    y1 = 0
                                y2 = y + int(1.1*h)
                                if y2 > hh :
                                    y2 = hh
                                    
                            # x direction extention
                            if ex+int(0.5*ew) > w-ex-int(0.5*ew):
                                print('x1')
                                x1 = int(x)
                                x2 = x+ 2*(ex+int(0.5*ew))
                                if x2 > ww :
                                    x2 = ww 
                            else :
                                print('x2')
                                x1 = x+w-2*(w-ex-int(0.5*ew))
                                if x1< 0 :
                                    x1= 0
                                x2 = x + int(w*1.1)
                                if x2 > ww:
                                    x2=ww 
                            return 1, image[ y1:y2, x1:x2]
    return 0, image

def sobelFilter(image):
    sobx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)  
    soby = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)   
    mag = np.hypot( sobx, soby)  # magnitude
    mag *= 255.0 / np.max(mag)  # normalize (Q&D)
    mag = mag.astype( np.uint8)
    return mag

def dataAugmentation( img,filename):
    datagen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        zoom_range=0.2,
        fill_mode='nearest')
    
    x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
    x = x.reshape((1,) + x.shape)  # this is a Numpy array with shape (1, 3, 150, 150)
    # the .flow() command below generates batches of randomly transformed images
    # and saves the results to the `preview/` directory
    i = 0
    for batch in datagen.flow(x, batch_size=1,
                              save_to_dir='male', save_prefix=filename, save_format='jpg'):
        i += 1
        if i > 20:
            break  # otherwise the generator would loop indefinitely
        
def cascade():
    face_cascade = []
    face_cascade.append(cv2.CascadeClassifier('haarcascade_profileface.xml'))
    face_cascade.append(cv2.CascadeClassifier('haarcascade_frontalface_default.xml'))
    face_cascade.append(cv2.CascadeClassifier('haarcascade_frontalface_alt.xml'))
    face_cascade.append(cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml'))
    face_cascade.append(cv2.CascadeClassifier('haarcascade_frontalface_alt_tree.xml'))
    eye_cascade = []
    eye_cascade.append(cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml'))
    #eye_cascade.append(cv2.CascadeClassifier('haarcascade_eye.xml'))
    return face_cascade, eye_cascade
def main():
    face_cascade,eye_cascade = cascade()  
    adultmfile = glob.glob("male/*.jpg")
    for file in adultmfile :
       # print(file)
        img = cv2.imread(file)
        find, img = findFace( face_cascade, eye_cascade, img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    
        if find == 1 :
            #mag = sobelFilter(gray)
            #print(mag.shape)
            #mag = cv2.resize(mag,(60,60), interpolation=cv2.INTER_AREA)
            #cv2.imshow(file[4:], gray)
            cv2.imwrite(file[5:],gray)
            dataAugmentation(gray, file[5:-4])
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
        else :
            print('cant find')
    
if __name__ == "__main__":
    main()

