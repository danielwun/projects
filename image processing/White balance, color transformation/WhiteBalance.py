from skimage import io, color
import numpy as np

def rgb_to_lab( rgb ):
    # from easyRGB
    # refer to a D65/2° standard illuminant.
    lab = []
    for i in range(rgb.shape[0]):
        lab.append([])
        for j in range(rgb.shape[1]):
            var_R = ( rgb[i][j][0] / 255 )
            var_G = ( rgb[i][j][1] / 255 )
            var_B = ( rgb[i][j][2] / 255 )

            if ( var_R > 0.04045 ):
                var_R = ( ( var_R + 0.055 ) / 1.055 ) ** 2.4
            else:
                var_R = var_R / 12.92
            if ( var_G > 0.04045 ):
                var_G = ( ( var_G + 0.055 ) / 1.055 ) ** 2.4
            else:
                var_G = var_G / 12.92
            if ( var_B > 0.04045 ):
                var_B = ( ( var_B + 0.055 ) / 1.055 ) ** 2.4
            else :
                var_B = var_B / 12.92

            var_R = var_R * 100
            var_G = var_G * 100
            var_B = var_B * 100

            X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
            Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
            Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505

            
            var_X = X / 95.047
            var_Y = Y / 100.000
            var_Z = Z / 108.883

            if ( var_X > 0.008856 ):
                var_X = var_X ** ( 1/3 )
            else:
                var_X = ( 7.787 * var_X ) + ( 16 / 116 )
            if ( var_Y > 0.008856 ):
                var_Y = var_Y ** ( 1/3 )
            else:
                var_Y = ( 7.787 * var_Y ) + ( 16 / 116 )
            if ( var_Z > 0.008856 ):
                var_Z = var_Z ** ( 1/3 )
            else:
                var_Z = ( 7.787 * var_Z ) + ( 16 / 116 )

            L = ( 116 * var_Y ) - 16
            a = 500 * ( var_X - var_Y )
            b = 200 * ( var_Y - var_Z )
            lab[i].append([L,a,b])
    return np.array(lab)

def lab_to_rgb (lab) :
    rgb = []
    for i in range(lab.shape[0]):
        rgb.append([])
        for j in range(lab.shape[1]):
            var_Y = ( lab[i,j,0] + 16 ) / 116
            var_X = lab[i,j,1] / 500 + var_Y
            var_Z = var_Y - lab[i,j,2] / 200

            if ( var_Y**3  > 0.008856 ):
                var_Y = var_Y**3
            else :
                var_Y = ( var_Y - 16 / 116 ) / 7.787
            if ( var_X**3  > 0.008856 ) :
                var_X = var_X**3
            else :
                var_X = ( var_X - 16 / 116 ) / 7.787
            if ( var_Z**3  > 0.008856 ):
                var_Z = var_Z**3
            else :
                var_Z = ( var_Z - 16 / 116 ) / 7.787

            X = var_X * 95.047
            Y = var_Y * 100.000
            Z = var_Z * 108.883

            var_X = X / 100
            var_Y = Y / 100
            var_Z = Z / 100

            var_R = var_X *  3.2406 + var_Y * -1.5372 + var_Z * -0.4986
            var_G = var_X * -0.9689 + var_Y *  1.8758 + var_Z *  0.0415
            var_B = var_X *  0.0557 + var_Y * -0.2040 + var_Z *  1.0570

            if ( var_R > 0.0031308 ):
                var_R = 1.055 * ( var_R ** ( 1 / 2.4 ) ) - 0.055
            else :
                var_R = 12.92 * var_R
            if ( var_G > 0.0031308 ) :
                var_G = 1.055 * ( var_G ** ( 1 / 2.4 ) ) - 0.055
            else :
                var_G = 12.92 * var_G
            if ( var_B > 0.0031308 ) :
                var_B = 1.055 * ( var_B ** ( 1 / 2.4 ) ) - 0.055
            else :
                var_B = 12.92 * var_B
            sR = var_R*255
            sG = var_G*255
            sB = var_B*255
            if( sR>255 ):
                sR = 255
            elif( sR<0 ):
                sR = 0
            if( sG>255 ):
                sG = 255
            elif( sG<0 ):
                sG = 0
            if( sB>255 ):
                sB = 255 
            elif( sB<0 ):
                sB = 0
            rgb[i].append([sR,sG,sB])
    return np.array(rgb,dtype=np.uint8)

def average( lab ):
    size = lab.shape[0] * lab.shape[1]
    suma = np.sum( lab[:,:,1] )
    sumb = np.sum( lab[:,:,2] )
    suma /= size
    sumb /= size
    return suma, sumb

def whiteBalance( lab, shifta , shiftb):
    parameter = 1.5
    deltaa = np.copy(lab[:,:,0]) * shifta * parameter / 100
    deltab = np.copy(lab[:,:,0]) * shiftb * parameter / 100
    lab[:,:,1] -= deltaa
    lab[:,:,2] -= deltab
    return lab

def main():
    image1 = io.imread("input1.bmp")    # mode= RGB
    simage = np.copy( image1 )
    simage = rgb_to_lab(simage)
    avera , averb = average( simage )   #get the average number of RGB
    simage = whiteBalance( simage, avera, averb )
    simage = lab_to_rgb(simage)
    
    io.imsave("wb.bmp", simage )
    
if __name__== "__main__":
    main()

