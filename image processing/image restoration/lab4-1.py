from skimage import io
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math
import matplotlib.pyplot as plt

def showgraph(image):
    z  = np.copy(image)
    z = np.abs(z)
    length = z.shape[0]
    width = z.shape[1]
    x = np.linspace( -math.pi, math.pi, width )
    y = np.linspace( -math.pi, math.pi, length )
    x, y = np.meshgrid( x, y )
    x = x.reshape(length*width)
    y = y.reshape(length*width)
    z = z.reshape(length*width)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, s=1 , c='r', marker='o')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()
    
def gaussian( sigma, x, y ):
    g = math.exp( -(x**2+y**2)/(2*sigma**2) )/ ( (2*math.pi)*sigma**2 )
    return g

def make_gfilter( sigma, n ):
    gfilter = np.zeros((n,n))
    X = np.linspace( int(-n/2) , int(n/2), n )
    print(X)
    for x in X :
        for y in X :
            gfilter[ int(y+n/2-1), int(x+n/2-1) ] = gaussian( sigma, x, y)
    return gfilter

def expandgaussian( gaussian, length, width ):
    egaussian = np.zeros( (length, width) )
    for i in range( gaussian.shape[0] ) :
        for j in range( gaussian.shape[1] ):
            egaussian[ int(length/2)-int(gaussian.shape[0]/2)+i, int(width/2)-int(gaussian.shape[1]/2)+j  ] = gaussian[i,j] 
    
    return egaussian    

def PSNR( image, target ):
    length = image.shape[0]
    width = image.shape[1]
    mse = [0,0,0]
    for i in range(length):
        for j in range(width):
            for k in range(3):
                mse[k] += (image[i,j,k]-target[i,j,k])**2
    
    mse = np.array(mse)* 255**2/(length*width)
    mse = np.sum( 10*np.log((255**2)/mse))
    return mse

def wiener( ffilter, fimage, k ):
    H = (1/ffilter)*(np.abs(ffilter)**2)/(np.abs(ffilter)**2 + k )
    #print(H)
    return np.multiply( H, fimage)

def main():
    target = np.array( io.imread("input1_ori.bmp"), dtype = float)/255
    image = np.array( io.imread("input1.bmp"), dtype=float)      # RGB
    gaussian = make_gfilter( 8, 101 )
    gaussian /= np.sum(gaussian)        #normalization
    #expand gaussian mask to the image size
    egaussian = expandgaussian( gaussian, image.shape[0], image.shape[1])
    imager = np.fft.fft2( image[:,:,0] )       #2D fft
    imageg = np.fft.fft2( image[:,:,1] )
    imageb = np.fft.fft2( image[:,:,2] )
    
    
    egaufft = np.fft.fft2(egaussian)       #fouriers transform
    egaufft = np.abs( egaufft )         #find the magnitude
    H =  np.amax(egaufft) / egaufft
    np.clip( H, 1, 2, out=H)

    b = np.fft.fftshift( egaufft )  #put frequency (0. , 0.) to middle
    io.imshow( 20*np.log(b+1), cmap='gray')
    plt.show()

    b = np.fft.fftshift( H )  #put frequency (0. , 0.) to middle
    io.imshow( 20*np.log(b), cmap='gray')
    plt.show()

    '''
    for i in range( egaufft.shape[0] ):
        for j in range( egaufft.shape[1]):
            if( egaufft[i,j]== 0 ):
                    egaufft[i,j] = 0.0001
    
    #print(egaufft)
    
    #showgraph(egaufft)
    
    #inverse filter
    '''
    imager = np.multiply( imager, H )
    imageg = np.multiply( imageg, H )
    imageb = np.multiply( imageb, H )

    a = 20*np.log(np.abs(np.fft.fftshift( imageb ))+1)
    #showgraph(a)
    io.imshow(a,cmap='gray')
    plt.show()

    #imager = wiener( egaufft, imager, 0.05 )
    #imageg = wiener( egaufft, imageg, 0.05 )
    #imageb = wiener( egaufft, imageb, 0.05 )   

    imager = np.fft.ifft2( imager )     #inverse 2D fft
    imageg = np.fft.ifft2( imageg )
    imageb = np.fft.ifft2( imageb )
    image2 = np.dstack((imager,imageg))
    image2 = np.dstack((image2,imageb))
    image2 = np.abs(image2)
    
    #print(image.shape)
    for i in range(image2.shape[0]):
        for j in range( image2.shape[1]):
            for k in range(3):
                if ( image2[i,j,k]>255 ):
                    image2[i,j,k] = 255
    #showgraph(image)
    image /= 255         
    image2 /= 255
    print( PSNR(image2,target) )
    print( PSNR(image,target) )
    print( PSNR(image2,target)/PSNR(image,target) )
    io.imsave("output1-2.bmp",image2 )
    
if __name__== "__main__":
    main()

