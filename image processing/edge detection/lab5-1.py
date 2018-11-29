from skimage import io
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy import signal
import cv2

def rgb2gray( rgb ):
    return np.dot( rgb, [ 0.299,0.587, 0.114 ] ) ;

def nonmaxima_suppression( Mxy, theta ):
    length = Mxy.shape[0]
    width = Mxy.shape[1]
    temp = np.zeros( (length, width) )
    temp[1:length-1, 1:width-1 ] = Mxy[1:length-1,1:width-1]
    for i in range(1,length-1) :
        for j in range(1,width-1) :
            if( theta[i,j]<=22.5 or theta[i,j]>=157.5 ):
                if( ( temp[i,j+1] > temp[i,j]) or (temp[i,j-1] > temp[i,j]) ):
                   temp[i,j] = 0
            elif( theta[i,j]>22.5 and theta[i,j]<=67.5 ):
                if( (temp[i,j] < temp[i-1,j+1]) or (temp[i,j] < temp[i+1,j-1]) ):
                    temp[i,j] = 0
            elif( theta[i,j]>67.5 and theta[i,j]<=112.5 ):
                if( (temp[i,j] < temp[i+1,j]) or (temp[i,j] < temp[i-1,j]) ):
                    temp[i,j] = 0
            elif( theta[i,j]>112.5 and theta[i,j]<=157.5 ):
                if( (temp[i,j] < temp[i+1,j+1]) or (temp[i,j] < temp[i-1,j-1]) ):
                    temp[i,j] = 0
    return temp

def threshold( Mxy, TH ,TL ):
    length = Mxy.shape[0]
    width = Mxy.shape[1]
    for i in range(1,length-1) :
        for j in range(1,width-1) :
            if ( Mxy[i,j] < TL ):
                Mxy[i,j] = 255
            elif( Mxy[i,j] < TH and Mxy[i,j] >= TL ):
                if( (Mxy[i-1,j-1]>=TH or Mxy[i-1,j]>=TH or Mxy[i-1,j+1]>=TH or Mxy[i,j-1]>=TH or Mxy[i,j+1]>=TH or Mxy[i+1,j-1]>=TH or Mxy[i+1,j]>=TH or Mxy[i+1,j+1]>=TH) ):
                    Mxy[i,j] = 0
                else:
                    Mxy[i,j] = 255
            else:
                Mxy[i,j]=0
    return Mxy
def markup( img, mark ):
    for i in range(img.shape[0]) :
        for j in range(img.shape[1]) :
            if( mark[i,j]==0 ):
                img[i,j] = [255,0,0]
    return img
def main():
    image = np.array( io.imread("input1.jpg"), dtype=float)      # RGB
    bimage = cv2.GaussianBlur( image, (5,5), 0)
    bimage = rgb2gray(bimage)
    # gradient
    gx = np.array([[ -1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    gy = np.transpose(gx)
    imagex = signal.convolve2d( bimage, gx, boundary='symm', mode='same')
    imagey = signal.convolve2d( bimage, gy, boundary='symm', mode='same')
    Mxy = np.sqrt( np.square(imagex) + np.square(imagey))
    print( np.amax(Mxy),' ',np.amin(Mxy))
    theta = np.arctan2( imagey, imagex )*180/np.pi 
    np.absolute( theta, theta )
    # nonmaxima suppression
    Mxy = nonmaxima_suppression( Mxy, theta )
    canny = threshold( Mxy, 70, 60 );
    print( np.amax(canny),' ',np.amin(canny))
    image = markup(image, canny)
    io.imsave("output.jpg", image/255 )
    
if __name__== "__main__":
    main()

