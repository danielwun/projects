#ifndef MONSTER_H
#define MONSTER_H
#include<ctime>
#include"Character.h"
#define width 21
class Monster:public Character{
	public:
		
		Monster( int,int,int) ;   //Constructer
		void Move() ;			  //automatically move 
		virtual void print(Cell [][width]) ;
								  //virtual print 
	private:
		int originalx ;
		int originaly ;
};
#endif
