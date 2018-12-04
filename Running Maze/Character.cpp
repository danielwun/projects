#include"Character.h"
#include<iostream>
using namespace std ;
Character::Character(int a=0, int b=0, int s=0){
	x = a ;
	y = b ;
	speed = s ;
}
void Character::setX(int a){
	x = a ;
}
void Character::setY(int b){
	y = b ;
}
void Character::setSpeed(int s){
	speed = s ; 
}
int Character::getX() {
	return x ;
}
int Character::getY() {
	return y ; 
}
int Character::getSpeed() {
	return speed ;
}

void gotoxy(int posX, int posY){
    COORD scrn;
    HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    scrn.X = posX; scrn.Y = posY;
    SetConsoleCursorPosition(hOut,scrn);
}
void SetColor(int f,int b){
    unsigned short ForeColor=f+16*b;
    HANDLE hCon = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hCon,ForeColor);
}

