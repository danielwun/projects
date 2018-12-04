#ifndef HERO_H
#define HERO_H
#include"Character.h"
#define NUM 21
class Hero: public Character {
	public:
		Hero(int,int,int) ;		// Constucter
		void readMove(int) ;	
						// up =1 down =2 left =3 right =4 
		virtual	void print(Cell[][NUM])  ; 
								//virtual print  
		bool getEnd();
							//arrive at end or not
	private: 
		int originalx ;
		int originaly ;
		bool end;
};

#endif
