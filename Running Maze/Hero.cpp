#include<iostream>
#include<ctime>
#include"Hero.h"
#define SIZE 21
using namespace std ;
Hero::Hero(int x=0,int y=0,int s=1):Character(x,y,s){
	originalx = getX() ;
	originaly = getY() ;
	end = false ;
}
void Hero::readMove(int dir){
	originalx = getX() ;
	originaly = getY() ;
	switch(dir){
		case 1 :
			if( getY()-getSpeed() > 0 )		
				setY( getY()-getSpeed() ) ;
			break ;
		case 2 :
			if( getY()+getSpeed() < SIZE-1 )
				setY( getY()+getSpeed() ) ;
			break ;
		case 3 :
			if( getX()-getSpeed() > 0 )
				setX( getX()-getSpeed() ) ;
			break ;
		case 4 :
			if( getX()+getSpeed() < SIZE-1 )
				setX( getX()+getSpeed() ) ;
			break ;
	}
	if(getX()==1 && getY()==1)
		end = true ;
}
void Hero::print(Cell level[][NUM]){
	int x , y ;
	x = getX() ;
	y = getY() ;
	gotoxy(2*originalx+1,originaly+1) ;
	cout<<"O" ;	
	if( originalx == x ){
		if( originaly > y ){
			for(int i=1 ; i<=getSpeed() ; i++){
				if( (originaly+i)<NUM ){ 
					if( level[originaly-i][originalx].display==' ' ){
						gotoxy(2*originalx+1,originaly+1) ;
						cout<<" " ;
						gotoxy(2*originalx+1,originaly-i+1) ;
						cout<<"O" ;	
						setY(originaly-i) ;	
					}else if(level[originaly-i][originalx].display=='*' ){
						gotoxy(2*originalx+1,originaly-i+1) ;
						SetColor(4,0) ;
						cout<<"*" ;
						SetColor() ;
						level[originaly-i][originalx].life-- ;
						if(level[originaly-i][originalx].life==0){
							level[originaly-i][originalx].display=' ' ;
							cout<<" " ;
							setY(originaly-i+1) ;
						}else{
							gotoxy(2*originalx+1,originaly-i+1) ;
							Sleep(100) ;
							cout<<"*" ;
							setY(originaly-i+1) ;
						} 
						break ;
					}
				}else{
					break ;
				}
			}
		}else if(originaly < y ){
			for(int i=1 ; i<=getSpeed() ; i++){
				if(originaly+i>0){
					if( level[originaly+i][originalx].display==' ' ){
						gotoxy(2*originalx+1,originaly+1) ;
						cout<<" " ;	
						gotoxy(2*originalx+1,originaly+i+1) ;
						cout<<"O" ;	
						setY(originaly+i) ;
					}else if(level[originaly+i][originalx].display=='*'){
						gotoxy(2*originalx+1,originaly+i+1) ;
						SetColor(4,0) ;
						cout<<"*" ;
						SetColor() ;
						setY(originaly+i-1) ;
						level[originaly+i][originalx].life-- ;
						if(level[originaly+i][originalx].life==0){
							level[originaly+i][originalx].display=' ' ;
							gotoxy(2*originalx+1,originaly+i+1) ;
							cout<<" " ;
						}else{ 
							Sleep(100) ;
							gotoxy(2*originalx+1,originaly+i+1) ;
							cout<<"*" ;
						}
						break ;
					}
				}else{
					break ;
				}
			}
		}
	}else{
		if( originalx < x ){//right
			for(int i=1 ; i<=getSpeed() ; i++){
				if( (originalx+i) < NUM ){
					if( level[originaly][originalx+i].display==' ' ){
						gotoxy(2*originalx+1,originaly+1) ;
						cout<<" " ;
						gotoxy(2*originalx+1+2*i,originaly+1) ;
						cout<<"O" ;
						setX(originalx+i) ;
					}else if(level[originaly][originalx+i].display=='*'){
						SetColor(4,0) ; 
						gotoxy(2*originalx+1+2*i,originaly+1) ;
						cout<<"*" ;
						SetColor() ; 
						level[originaly][originalx+i].life-- ;
						if(level[originaly][originalx+i].life==0){
							level[originaly][originalx+i].display=' ' ;
							gotoxy(2*originalx+1+2*i,originaly+1) ;
							cout<<" " ;
							setX(originalx+i-1) ;
						}else{ 
							Sleep(100) ;
							gotoxy(2*originalx+1+2*i,originaly+1) ;
							cout<<"*" ;
							setX(originalx+i-1) ;
						} 
						break ;
					}
				}else{
					break ;
				}
			}
		}else if(originalx > x){
			for(int i=1 ; i<=getSpeed() ; i++){
				if((originalx-i)>0){
					if( level[originaly][originalx-i].display==' ' ){
						gotoxy(2*originalx+1,originaly+1) ;
						cout<<" " ;	
						gotoxy(2*originalx+1-2*i,originaly+1) ;
						cout<<"O" ;	
						setX(originalx-i) ;	
					}else if(level[originaly][originalx-i].display=='*'){
						SetColor(4,0) ; 
						gotoxy(2*originalx+1-2*i,originaly+1) ;
						cout<<"*" ;
						SetColor() ;
						level[originaly][originalx-i].life-- ;
						if(level[originaly][originalx-i].life==0){
							level[originaly][originalx-i].display=' ' ;
							gotoxy(2*originalx+1-2*i,originaly+1) ;
							cout<<" " ;
							setX(originalx-i+1) ;
						}else{
							Sleep(100) ; 
							gotoxy(2*originalx+1-2*i,originaly+1) ;
							cout<<"*" ;
							setX(originalx-i+1) ;
						} 
						break ;
					}
				}else{
					break ;
				}
			}
		}	
	}
}

bool Hero::getEnd()
{	
	return end ;
}
