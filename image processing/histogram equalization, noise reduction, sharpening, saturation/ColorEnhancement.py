from skimage import io
import numpy as np
import math
import matplotlib.pyplot as plt

def rgb_to_hsi( rgb ):
    #R, G and B input range = 0 ÷ 255
    #H, S and L output range = 0 ÷ 1.0
    hsi = np.copy(rgb)/255  #( 450, 300, 3 )
    for i in range(hsi.shape[0] ):
        for j in range(hsi.shape[1]):
            I = np.sum(hsi[i,j]) *255 / 3
            den = 2*math.sqrt( (hsi[i,j,0]-hsi[i,j,1])**2+(hsi[i,j,0]-hsi[i,j,2])*(hsi[i,j,1]-hsi[i,j,2]) )
            if( den == 0 ):
                H = 0
            else:
                ans = (2*hsi[i,j,0]-hsi[i,j,1]-hsi[i,j,2])/den
                if( ans>1 ):
                    ans = 1
                elif ( ans<-1 ):
                    ans = -1
                H = 180 * math.acos( ans )/math.pi
                if( hsi[i,j,1] < hsi[i,j,2] ):
                    H = 360 - H
            if( I == 0 ):
                S = 0
            else:
                S = 1 - np.amin(hsi[i,j])*255/I
                
            hsi[i,j] = np.array([H,S,I])
    return hsi

def hsi_to_rgb (hsi) :
    rgb = np.copy(hsi)
    for i in range(rgb.shape[0]) :
        for j in range(rgb.shape[1]) :
            if( rgb[i,j,0]>=0 and rgb[i,j,0]<120 ):
                b = (1-rgb[i,j,1])/3
                r = (1+rgb[i,j,1]*math.cos(rgb[i,j,0]*math.pi/180)/math.cos((60-rgb[i,j,0])*math.pi/180))/3
                g = 1 - b - r
            elif( rgb[i,j,0]>=120 and rgb[i,j,0]<240 ):
                rgb[i,j,0] -= 120
                r = (1-rgb[i,j,1])/3
                g = (1+rgb[i,j,1]*math.cos(rgb[i,j,0]*math.pi/180)/math.cos((60-rgb[i,j,0])*math.pi/180))/3
                b = 1 - g - r
            elif( rgb[i,j,0]>=240 and rgb[i,j,0]<=360 ):
                rgb[i,j,0] -= 240
                g = (1-rgb[i,j,1])/3
                b = (1+rgb[i,j,1]*math.cos(rgb[i,j,0]*math.pi/180)/math.cos((60-rgb[i,j,0])*math.pi/180))/3
                r = 1 - b - g
                
            r *= 3*rgb[i,j,2]
            g *= 3*rgb[i,j,2]
            b *= 3*rgb[i,j,2]
            rgb[i,j] = np.array([r,g,b])
            for a in range(3):
                if ( rgb[i,j,a] > 255 ):
                    rgb[i,j,a] = 255
                elif( rgb[i,j,a] < 0 ):
                    rgb[i,j,a] = 0
    return np.array( rgb, dtype = np.uint8)

def histogramEqualization(hsi,power):
    gray = histogram(hsi)
    x = np.linspace(0,255,num=256)
    plt.bar(x, gray, 1/1.5, color="blue")
    plt.savefig("figure10.png")
    #plt.show()
    T = (Tr(gray)**power)*255
    plt.bar(x, T, 1/1.5, color="green")
    plt.savefig("figure11.png")
    #plt.show()
    for i in range(hsi.shape[0]):
        for j in range(hsi.shape[1]):
            hsi[i,j,2] = T[ int(round(hsi[i,j,2])) ]
    plt.close()
    gray = histogram(hsi)
    plt.bar(x, gray, 1/1.5, color="black")
    plt.savefig("figure12.png")
    #plt.show()
    return hsi
#def matching( img, power ):
    
def Tr(gray):
    T = np.zeros(256)
    T[0] = gray[0]
    for i in range(1,gray.shape[0]):
        T[i] = T[i-1] + gray[i]
    for i in range(gray.shape[0]):
        T[i] = (T[i])
    return T

def histogram(hsi):
    gray = np.zeros(256)
    size = hsi.shape[0]*hsi.shape[1]
    for i in range(hsi.shape[0]):
        for j in range(hsi.shape[1]):
            gray[ int(round(hsi[i,j,2])) ] += 1
    return gray/size    #normalize

def reduceNoise(img):
    mask = np.array([[1,4,7,4,1],[4,16,26,16,4],[7,26,41,26,7],[4,16,26,16,4],[1,4,7,4,1]])
    new = np.zeros( img.shape )
    heigth = img.shape[0]
    width = img.shape[1]
    for i in range(heigth):
        for j in range(width):
            if( i<2 ):
                if( j<2 ):
                    tmask = np.copy( mask[2-i:5,2-j:5] )
                elif( (width-1-j)<2 ):
                    tmask = np.copy( mask[2-i:5,0:1+width-j] )
                else:
                    tmask = np.copy( mask[2-i:5,:] )
            elif( heigth-1-i<2 ):
                if( j<2 ):
                    tmask = np.copy( mask[0:1+heigth-i,2-j:5] )
                elif( (width-1-j)<2):
                    tmask = np.copy( mask[0:1+heigth-i,0:1+width-j] )
                else:
                    tmask = np.copy( mask[0:1+heigth-i,:] )
            else:
                if( j<2 ):
                    tmask = np.copy( mask[:,2-j:5] )
                elif( (width-1-j)<2):
                    tmask = np.copy( mask[:,0:1+width-j] )
    
            tmask = tmask / np.sum(tmask)
             #find the starting coordination
            for c in range(3):
                if( (i-c) == 0 ):
                    break
            for r in range(3):
                if( (j-r) == 0 ):
                    break
            # masking
            #print(i,j," c= ",c," r= ",r," height= ", tmask.shape[0]," width= ", tmask.shape[1])
            for ii in range( tmask.shape[0] ):
                for jj in range( tmask.shape[1] ):
                    for a in range( img.shape[2] ):
                        new[ i, j, a ] += img[ i+ii-c, j+jj-r, a ]*tmask[ii,jj]
                        if( new[ i, j, a ]>255 ):
                            new[ i, j, a ]=255
    return new
def sharpening(img):
   #in rgb mode
    mask = np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
    sth = np.zeros(img.shape)
    heigth = img.shape[0]
    width = img.shape[1]
    for i in range(heigth):
        for j in range(width):
            if( i<1 ):
                if( j<1 ):
                    tmask = np.copy( mask[1-i:3,2-j:3] )
                elif( (width-1-j)<1 ):
                    tmask = np.copy( mask[1-i:3,0:width-j] )
                else:
                    tmask = np.copy( mask[1-i:3,:] )
            elif( heigth-1-i<1 ):
                if( j<1 ):
                    tmask = np.copy( mask[0:heigth-i,1-j:3] )
                elif( (width-1-j)<1):
                    tmask = np.copy( mask[0:heigth-i,0:width-j] )
                else:
                    tmask = np.copy( mask[0:heigth-i,:] )
            else:
                if( j<1 ):
                    tmask = np.copy( mask[:,1-j:3] )
                elif(( width-1-j)<2):
                    tmask = np.copy( mask[:,0:width-j] )
    
            tmask = tmask / np.sum(tmask)
             #find the starting coordination
            for c in range(2):
                if( (i-c) == 0 ):
                    break
            for r in range(2):
                if( (j-r) == 0 ):
                    break
            # masking
            #print(i,j," c= ",c," r= ",r," height= ", tmask.shape[0]," width= ", tmask.shape[1])
            for ii in range( tmask.shape[0] ):
                for jj in range( tmask.shape[1] ):
                    #for a in range( img.shape[2] ):
                    sth[ i, j, 2 ] += img[ i+ii-c, j+jj-r, 2]*tmask[ii,jj]
    img = img + sth
    for i in range(heigth):
        for j in range(width):
            #for a in range(3):
            if( img[i,j,2]>255 ):
                img[i,j,2]=255
            elif( img[i,j,2]<0 ):
                img[i,j,2]=0
    return img


def saturation(img, scale):
    #0~2 scale
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i,j,1]*=scale
            if( img[i,j,1]>1 ):
                img[i,j,1] = 1
    return img
def main():
    image1 = io.imread("input4.bmp")    # RGB
    simage = np.copy( image1 )
    #simage = reduceNoise( simage )
    simage = rgb_to_hsi(simage)
    #simage = histogramEqualization(simage,1.7)
    #simage = sharpening(simage)
    #simage = saturation(simage,1.5)
    simage = hsi_to_rgb(simage)
    io.imsave("output4-sharp.bmp", simage/255 )
    
if __name__== "__main__":
    main()

