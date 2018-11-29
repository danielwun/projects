#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

typedef struct BmpHeader{ 
	unsigned short id;      // there are a 2 bytes padding
    unsigned int fsize;		//file size,           
    unsigned int reserved;          
    unsigned int offset; 
    unsigned int hsize;		//Info Header size 
    int width;             
    int height;            
    unsigned short planes;          
    unsigned short bits;   
    unsigned int compression;       
    unsigned int imsize;   	//image size
    int xresolution;       
    int yresolution;       
    unsigned int ncolours;        
    unsigned int icolours;   
//    unsigned int palette;           
}__attribute__((packed)) BmpHeader;

int readBmpHeader( char* filename, BmpHeader* bh ){
	FILE *ifile;
	unsigned char *ptr ;
	ptr = (unsigned char*) bh ;
	ifile = fopen( filename , "rb" ) ;
	
	if( ifile == NULL ){
		printf("No such file on this directory!\n") ;
		return 0;
	}
	// To fix the problem of padding
	fread( ptr, sizeof(unsigned char), sizeof(unsigned short), ifile ) ;
	ptr = &bh->fsize;
	fread( ptr, sizeof(unsigned char), sizeof(BmpHeader)-4, ifile ) ;
	fclose(ifile) ;
	return 1;
}

void readBmpImage( char* filename, BmpHeader *bh, unsigned char* image, int complement){
	FILE *ifile;
	ifile = fopen( filename, "rb") ;
	fseek ( ifile , bh->offset , SEEK_SET );
	int i = 0 ;
	for( i=0 ; i < bh->height ; i++ ){
		fread( image, sizeof(unsigned char), bh->width*bh->bits/8, ifile) ;
		fseek( ifile, complement, SEEK_CUR) ;
		image = image + bh->width*bh->bits/8 + complement ;
	}
	fclose(ifile) ;
}

void readBmpPalette( char* filename, BmpHeader *bh, unsigned char* palette){
	FILE *ifile;
	ifile = fopen( filename, "rb") ;
	fseek ( ifile , 54 , SEEK_SET );
	fread( palette, sizeof(unsigned char), bh->offset-54, ifile) ;
	fclose(ifile) ;
}

void changeFilename( char** ofilename, char* filename, char* mesg){
	*ofilename = (char*)malloc( sizeof(char)*(strlen(filename)+strlen(mesg)+1+1) );
	strcpy(*ofilename, "./out") ;
	strcat( *ofilename, filename+4 ) ;
	char extension[strlen(mesg)+5] ;
	strcpy( extension,"_") ;
	strcat( extension, mesg) ;
	strcat( extension, ".bmp") ;
	strcpy( *ofilename+strlen(*ofilename)-4 , extension ) ;
}

void writeBmp( char* ofilename, const BmpHeader* bh, const unsigned char* palette, const unsigned char* image, int complement, int palebyte ){
	FILE *ofile ;
	unsigned char* ptr;
	ofile = fopen( ofilename, "wb") ;	
	if( ofile==NULL){
		printf("Open file fails\n") ;
		return ;
	}
//	Write Header 
	ptr = (unsigned char*) bh;
	fwrite( ptr, sizeof(unsigned char), sizeof(unsigned short), ofile) ;
	ptr = &bh->fsize ;
	fwrite( ptr, sizeof(unsigned char), sizeof(BmpHeader)-4, ofile) ;
//	Write palette
	fwrite( palette, sizeof(unsigned char), palebyte, ofile) ;
//	Write image
	int i ;
	short c ;
	char z = 0 ;
	for( i=0 ; i < bh->height ; i++  ){
		fwrite( image, sizeof(unsigned char), bh->width*bh->bits/8, ofile) ;
		for( c = complement ; c > 0 ; c-- ){
			fprintf( ofile,"%c",z) ;
		}
		image = image + bh->width*bh->bits/8 ;
	}
//	printf("output! success!\n") ;
	fclose(ofile) ;
}

void scalingUp( unsigned char*image, unsigned char* newimage, int width, int height, int pbyte, float factor ){
	int i, j, c , x, y;
	int swidth = (int)(width*factor) ;
	float xstep = (width-1)/(width*factor-1);
	float ystep=(height-1)/(height*factor-1) ;
	float dx, dy ;
//	printf("xs = %f  ys = %f\n",xstep,ystep) ;
//	printf("%d %d %d\n",(int)(height*factor), (int)(width*factor), pbyte) ;
	for( i=0 ; i< (int)(height*factor) ; i++ ){
		for( j=0 ; j< (int)(width*factor) ; j++){
			x = xstep*j/1 ; y = ystep*i/1 ;
			dx = xstep*j - x ;
			dy = ystep*i - y ; 
//			printf("x = %d , y = %d\n", x, y) ;
			for( c=0 ; c<pbyte ; c++ ){
				if( dx==0 && dy==0){
					newimage[ (int)(i*swidth*pbyte) + j*pbyte + c ] = image[ (int)(x*pbyte + y*width*pbyte + c)] ; 
				}else if( dx==0 ){
					newimage[ (int)(i*swidth*pbyte) + j*pbyte + c ] = 
						(int)( (1-dy)*image[ (int)(x*pbyte + y*width*pbyte + c)] + (dy)*image[ (int)(x*pbyte + (y+1)*width*pbyte + c)] ) ;
				}else if( dy==0 ){
					newimage[ (int)(i*swidth*pbyte) + j*pbyte + c ] = 
						(int)( (1-dx)*image[ (int)(x*pbyte + y*width*pbyte + c)] + (dx)*image[ (int)((x+1)*pbyte + y*width*pbyte + c)] ) ;
				}else{
						newimage[ (int)(i*swidth*pbyte) + j*pbyte + c ] = 
							(int)( (1-dx)*(1-dy)*image[ (int)(x*pbyte + y*width*pbyte + c)] + (dx)*(1-dy)*image[ (int)((x+1)*pbyte + y*width*pbyte + c)]
								+ (1-dx)*(dy)*image[ (int)(x*pbyte + (y+1)*width*pbyte + c)] + (dx)*(dy)*image[ (int)((x+1)*pbyte + (y+1)*width*pbyte + c)] ) ;
				}
			}
		}
	}
}

void rewriteBmpHeader( BmpHeader* bh , float factor, int complement ){
	bh->width = (int)(bh->width * factor) ;
	bh->height = (int)(bh->height * factor) ;
	bh->fsize = bh->fsize - bh->imsize + (int)(bh->width*bh->height*bh->bits/8 + complement*bh->height) ;
	bh->imsize = (int)(bh->width*bh->height*bh->bits/8) + complement*bh->height ;
}

int main(){
	BmpHeader ibmph ;	//input bmp header
	BmpHeader obmph	;	//output bmp header
	BmpHeader obmph2 ;
	
	char filename[] = "./input2.bmp" ;
//	Read Bmp file	
	readBmpHeader( filename, &ibmph) ;
	int imbyte = ibmph.width*ibmph.height*ibmph.bits/8 ;	
	unsigned char image[imbyte] ;
	int complement=0 ;
	if( (ibmph.width*ibmph.bits/8) % 4 !=0 ){
		complement = 4 - (ibmph.width*ibmph.bits/8) % 4 ;
	}
	readBmpImage( filename, &ibmph, image, complement) ; 
	
	unsigned char bpalette [ibmph.offset-54] ;
//	printf("%d \n",ibmph.offset-54) ;
	readBmpPalette( filename, &ibmph, bpalette ) ;
//	Done reading Bmp file

//	scaling
	obmph = ibmph ;
	char *ofilename ;
	changeFilename( &ofilename, filename, "up");
	float sfactor = 1.5;	//scaling factor
	int length = (int)(imbyte*sfactor*sfactor);
	unsigned char *upimage = (unsigned char*)malloc(sizeof(unsigned char)*length) ;
	complement = 0 ;
	if( (int)(ibmph.width*sfactor*ibmph.bits/8) % 4 !=0 ){
		complement = 4 - (int)(ibmph.width*sfactor*ibmph.bits/8) % 4 ;
	}
	
	scalingUp( image, upimage, ibmph.width, ibmph.height , ibmph.bits/8, sfactor) ;
	rewriteBmpHeader( &obmph , sfactor, complement );  
	writeBmp( ofilename, &obmph, bpalette, upimage, complement, ibmph.offset-54 );
//	Down
	free(ofilename) ;
	obmph2 = ibmph ;
	changeFilename( &ofilename, filename, "down");
	
	sfactor = 1/ sfactor ;
	int width = ibmph.width*sfactor;
	int height = ibmph.height*sfactor ;
	length = (int)(width*height*ibmph.bits/8) ;
	unsigned char *downimage = (unsigned char*)malloc(sizeof(unsigned char)*length) ;
	complement = 0 ;
	if( (int)( width*ibmph.bits/8 ) % 4 !=0 ){
		complement = 4 - (int)(width*ibmph.bits/8) % 4 ;
	}
	scalingUp( image, downimage, ibmph.width, ibmph.height , ibmph.bits/8, sfactor) ;
	rewriteBmpHeader( &obmph2 , sfactor, complement );  
	writeBmp( ofilename, &obmph2, bpalette, downimage, complement, ibmph.offset-54 );

//	Done scaling
	free(upimage) ;
	free(ofilename) ;
	free(downimage) ;
	return 0 ;
} 
