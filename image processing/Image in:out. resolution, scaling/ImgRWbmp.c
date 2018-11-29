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


void writeBmp( char* ofilename, const BmpHeader* bh, const unsigned char*palette, const unsigned char* image, int complement){
	FILE *ofile ;
	unsigned char* ptr;
	printf("%s\n", ofilename) ;
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
	fwrite(palette, sizeof(unsigned char), bh->offset-54, ofile) ;
//	Write image
	int i ;
	short c ;
	for( i=0 ; i < bh->height ; i++  ){
		fwrite( image, sizeof(unsigned char), bh->width*bh->bits/8, ofile) ;
		for( c = complement ; c > 0 ; c-- ){
			fprintf( ofile,"0") ;
		}
		image = image + bh->width*bh->bits/8 ;
	}
	printf("output! success!\n") ;
	fclose(ofile) ;
}

void changeFilename( char** ofilename, char* filename){
	*ofilename = (char*)malloc( sizeof(char)*(strlen(filename)+1) );
	sprintf( *ofilename,"./out%s",filename+4) ;
}

int main(){
	BmpHeader ibmph ;	//input bmp header
	BmpHeader obmph	;	//output bmp header
	
	char filename[] = "./input2.bmp" ;
//	Read Bmp file	
	readBmpHeader( filename, &ibmph) ;
	int imsize = ibmph.width*ibmph.height ;	
	unsigned char image[ibmph.width*ibmph.height*ibmph.bits/8] ;
	int complement=0 ;
	if( (ibmph.width*ibmph.bits/8) % 4 !=0 ){
		complement = 4 - (ibmph.width*ibmph.bits/8) % 4 ;
	}
	printf("complement= %d\n",complement) ;
	readBmpImage( filename, &ibmph, image, complement) ; 
	unsigned char bpalette [ibmph.offset-54] ;
	printf("%d ",ibmph.offset-54) ;
	readBmpPalette( filename, &ibmph, bpalette ) ;
//	Done reading Bmp file

//	Write Bmp file
	char *ofilename ;
	changeFilename( &ofilename, filename );
	printf("%s\n",ofilename) ;
	writeBmp(ofilename, &ibmph, bpalette, image, complement);
	
//	Done Writing
	
	return 0 ;
} 
