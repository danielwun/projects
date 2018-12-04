#ifndef CHARACTER_H
#define CHARACTER_H
#include"wall.h"
#include<windows.h>
class Character{
	public:
		Character(int ,int ,int) ;  //Constructer 
		
		void setX(int) ;			//set function
		void setY(int) ;			
		void setSpeed(int) ;		
		
		int getX () ;				//get function
		int getY () ;
		int getSpeed () ;
									//virtual print 
		virtual	void  print(Cell Level[][21])=0 ;
	
	protected:
		int x ;			
		int y ;				
		int speed ; 
};

void gotoxy(int , int ) ;			// change cout position 
void SetColor(int f=7,int b=0) ;	// change words' color

#endif 
