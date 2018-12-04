#include<iostream>
#include<ctime>
#include<windows.h>
#include<conio.h>
#include<stack>
#include<cstring>
#include"wall.h"
#include"Hero.h"
#include"Monster.h" 
#define SIZE 21
using namespace std ;

void Initialize( Cell Level[][SIZE] );  //initialize the maze
void ClearScreen();						//cout position to 0,0
void Redraw( Cell Level[][SIZE] );		//draw the moze
void GenerateMaze( Cell Level[][SIZE], int &posX , int &posY, int &goalX, int &goalY); 
										//generate the maze and draw
void MoveWall(Cell Level[][SIZE],int num, bool game_over);
										//wall random move


int main()
{
	Cell Level[SIZE][SIZE];
	int read ;
	int posX, posY ;
	int goalX, goalY ;
	int num_move_wall = 1 ;
	bool game_over = false ; 
	system("cls");
	Initialize(Level);
	Hero hero(SIZE-2, SIZE-2 , 1)  ;
	Monster monster1(3,3, 1 ), monster2(5,4, 1) ; 
	GenerateMaze(Level,posX,posY,goalX,goalY);
	hero.print(Level) ;
	Level[SIZE-2][SIZE-2].display = ' ';
	monster1.print(Level) ;
	monster2.print(Level) ;
	gotoxy(50,3);
	cout << "Hint : " ;
	gotoxy(50,4);
	cout << "Wall maybe disappear" ;
	gotoxy(52,5);
	cout << "if you hit 5 times" ; 
	gotoxy(50,11);
	cout << "press any key to start !" ;
	gotoxy(50,8);
	cout << "O is you " ;
	gotoxy(50,9);
	SetColor(4,0);
	cout << "O " ; 
	SetColor();
	cout << "is Monster ";
	gotoxy(50,10);
	cout << "E for EXIT " ;


	getch();
	gotoxy(50,11);
	cout << "press ESC to quit the game" ;
	gotoxy(50,12);
	cout << "press P to pause " ;

	while (!game_over)
	{
	
		MoveWall(Level, num_move_wall,game_over);
		if(kbhit()){
			read = getch() ;
		}
		switch(read){
			case 72:  
            	//up
				hero.readMove(1) ;
				break;  
        	case 75:  
            	//left 
            	hero.readMove(3) ;
				break;  
       		case 77:  
            	//right
				hero.readMove(4) ;  
          		break;  
       		case 80:       
            	//down 
            	hero.readMove(2) ;
				break;  
			case 27: //ESC
				game_over = true ;
				break ;
			case 112: // P
				gotoxy(50,11);
				cout << "press any key to resume !!";
				gotoxy(50,12);
				cout << "                  ";
				getch();
				break ;
		}
		read = 0 ; 
		monster1.Move() ;
		monster2.Move() ;
		
		if( (monster1.getX() == hero.getX() && monster1.getY() == hero.getY() ) || 
			(monster2.getX() == hero.getY() && monster2.getY() == hero.getY() ) )
		{
			game_over = true ;
			system("cls") ;
			gotoxy(21,5);
			cout << "Oh Idiot !"  ;
			gotoxy(21,6);
			cout << "YOU Loose !!!!!!"  ;
			getch();
		}
		
		hero.print(Level) ;
		monster1.print(Level) ;
		monster2.print(Level) ;
		
		
		
		if ( hero.getEnd() )
		{
			game_over = true ;
			system("cls") ;
			gotoxy(21,5);
			cout << "Congratulations !"  ;
			gotoxy(21,6);
			cout << "YOU WIN !!!!!!"  ;
			getch();
		}
	}
	system("cls");
	gotoxy(21,5);
	cout << "Have a nice day!!" ;
	getch();
	return 0 ;
}


void Initialize( Cell Level[][SIZE])
{
	for(int i=0; i<SIZE ; i++)
	{
		for (int j=0; j<SIZE; j++)
		{
			Level[i][j].display = '*';
			Level[i][j].visited = false ;
			Level[i][j].top_wall = true ;
			Level[i][j].bot_wall = true ;
			Level[i][j].left_wall = true ;
			Level[i][j].right_wall = true ;
			Level[i][j].life = 5 ;
		}
	}
	for(int i=1; i<SIZE-1; i++)
	{
		for(int j=1; j<SIZE-1; j++)
		{
			Level[1][j].top_wall = false ;
			Level[SIZE-2][j].bot_wall = false ;
			Level[i][1].left_wall = false ;
			Level[i][SIZE-2].right_wall = false ;
		}
	}
}

void ClearScreen()
{
	HANDLE hOut; 
	COORD Position;
	hOut = GetStdHandle(STD_OUTPUT_HANDLE);
	Position.X = 0 ;
	Position.Y = 0 ;
	SetConsoleCursorPosition(hOut, Position);
}

void Redraw(Cell Level[][SIZE])
{
	for(int i=0; i<SIZE; i++)
	{
		cout << endl ;
		for(int j=0; j<SIZE; j++)
		{
			cout << " " << Level[i][j].display ;
		}
	}
}

void GenerateMaze( Cell Level[][SIZE], int &posX, int &posY, int &goalX, int &goalY)
{
	srand ((unsigned)time(NULL));
	int random ;
	int randomX = (2*rand()+1) % (SIZE-1);
	int randomY = (2*rand()+1) % (SIZE-1);
	posX = 1;
	posY = 1;
	int visitedCells = 1;
	int totalCells = ((SIZE-1)/2)*((SIZE-1)/2);
	int percent;
	stack<int> back_trackX, back_trackY;
	
	while(visitedCells <= totalCells)
	{
		
		if(((Level[randomY-2][randomX].visited == false) &&(Level[randomY][randomX].top_wall == true) &&(Level[randomY-2][randomX].bot_wall == true)) ||
		   ((Level[randomY+2][randomX].visited == false) &&(Level[randomY][randomX].bot_wall == true) &&(Level[randomY+2][randomX].top_wall == true)) ||
		   ((Level[randomY][randomX-2].visited == false) &&(Level[randomY][randomX].left_wall == true) &&(Level[randomY][randomX-2].right_wall == true)) ||
		   ((Level[randomY][randomX+2].visited == false) &&(Level[randomY][randomX].right_wall == true) &&(Level[randomY][randomX+2].left_wall == true))) 
		{
			random = rand()%4 + 1; 
			
			if((random == 1) && (randomY > 1))                      //choose up
			{
				if((Level[randomY-2][randomX].visited == false))
				{
					Level[randomY-1][randomX].display = ' ';
					Level[randomY-1][randomX].visited = true;
					Level[randomY][randomX].top_wall = false;
					
					back_trackX.push(randomX);
					back_trackY.push(randomY);
					
					randomY -= 2 ;
					Level[randomY][randomX].visited = true ;
					Level[randomY][randomX].display = ' ';
					Level[randomY][randomX].bot_wall = false;
					visitedCells++;
				}
				else
					continue;
			}
			else if((random == 2) && (randomY < SIZE-2))            //choose down
			{
				if((Level[randomY+2][randomX].visited == false))
				{
					Level[randomY+1][randomX].display = ' ';
					Level[randomY+1][randomX].visited = true;
					Level[randomY][randomX].bot_wall = false;
					
					back_trackX.push(randomX);
					back_trackY.push(randomY);
					
					randomY += 2 ;
					Level[randomY][randomX].visited = true ;
					Level[randomY][randomX].display = ' ';
					Level[randomY][randomX].top_wall = false;
					visitedCells++;
				}
				else
					continue;
			}
			//GO LEFT
			else if((random == 3) && (randomX > 1))					
			{
				if((Level[randomY][randomX-2].visited == false))
				{
					Level[randomY][randomX-1].display = ' ';
					Level[randomY][randomX-1].visited = true;
					Level[randomY][randomX].left_wall = false;
					
					back_trackX.push(randomX);
					back_trackY.push(randomY);
					
					randomX -= 2 ;
					Level[randomY][randomX].visited = true ;
					Level[randomY][randomX].display = ' ';
					Level[randomY][randomX].right_wall = false;
					visitedCells++;
				}
				else
					continue;
			}
			//GO RIGHT
			else if((random == 4) && (randomX < SIZE-2))			
			{
				if((Level[randomY][randomX+2].visited == false))
				{
					Level[randomY][randomX+1].display = ' ';
					Level[randomY][randomX+1].visited = true;
					Level[randomY][randomX].right_wall = false;
					
					back_trackX.push(randomX);
					back_trackY.push(randomY);
					
					randomX += 2 ;
					Level[randomY][randomX].visited = true ;
					Level[randomY][randomX].display = ' ';
					Level[randomY][randomX].left_wall = false;
					visitedCells++;
				}
				else
					continue;
			}
			percent = (visitedCells*100/totalCells*100)/100;
			cout << endl << "   Generating a Random Maze ...." << percent << "%"  << endl;
		}
		else 
		{
			randomX = back_trackX.top();
			back_trackX.pop();
			
			randomY = back_trackY.top();
			back_trackY.pop();
		}
		ClearScreen();
		//Redraw(Level);
	}
	
	Level[posY][posX].display = 'E';
	Level[posY][posX].visited = true;
	goalX = SIZE - 2 ;
	goalY = SIZE - 2 ;

	system("cls");
	ClearScreen();
	Redraw(Level);

}	

void MoveWall(Cell Level[][SIZE], int num,bool game_over)
{	

	int randomX[num], randomY[num];
	int random;
	gotoxy(50,11);
	cout << "press ESC to quit the game" ;
	gotoxy(50,12);
	cout << "press P to pause " ;
	bool move=false ;	
	for(int i=0;i<num;i++)
		{
			randomX[i] = (rand() % (SIZE-2)) +1;
			randomY[i] = (rand() % (SIZE-2)) +1;
			while ( Level[randomY[i]][randomX[i]].display != '*' )
			{
				randomX[i] = rand() % (SIZE-2) +1;
				randomY[i] = rand() % (SIZE-2) +1 ;
			}
		}
		
		for(int i=0;i<num;i++)
		{
			random = rand()%4 + 1 ;
			// go up
			if(random == 1 &&  randomY[i] > 1)
			{
				if(Level[randomY[i]-1][randomX[i]].display == ' ')
				{
					Level[randomY[i]-1][randomX[i]].display = '*' ;
					Level[randomY[i]][randomX[i]].display = ' ' ;
				
					gotoxy(2*randomX[i]+1, randomY[i]-1+1 ) ;
					cout << Level[randomY[i]-1][randomX[i]].display ;
				
					gotoxy(2*randomX[i]+1, randomY[i] +1) ;
					cout << Level[randomY[i]][randomX[i]].display ;
					move = true;
				}
				else
					continue;
								
			}
			//go down
			else if( random == 2 &&  randomY[i] < SIZE-2 )
			{
				if(Level[randomY[i]+1][randomX[i]].display == ' ')
				{
					Level[randomY[i]+1][randomX[i]].display = '*' ;
					Level[randomY[i]][randomX[i]].display = ' ' ;
				
					gotoxy(2*randomX[i]+1, randomY[i]+1+1 ) ;
					cout <<  Level[randomY[i]+1][randomX[i]].display ;
					
					gotoxy(2*randomX[i]+1, randomY[i]+1 ) ;
					cout << Level[randomY[i]][randomX[i]].display ;
					move = true;
				}
				else
					continue;
			}
			//go left 
			else if(random == 3 && randomX[i] > 1)
			{
				if(Level[randomY[i]][randomX[i]-1].display == ' ')
				{
					Level[randomY[i]][randomX[i]-1].display = '*' ;
					Level[randomY[i]][randomX[i]].display = ' ' ;
				
					gotoxy(2*randomX[i]-1, randomY[i] +1) ;
					cout << Level[randomY[i]][randomX[i]-1].display ;
				
					gotoxy(2*randomX[i]+1, randomY[i] +1) ;
					cout << Level[randomY[i]][randomX[i]].display ;
					move = true;
				}
				else
					continue;
			}
			//go right 
			else if(random == 4 &&  randomX[i] < SIZE-2 )
			{
				if(Level[randomY[i]][randomX[i]+1].display == ' ')
				{
					Level[randomY[i]][randomX[i]+1].display = '*' ;
					Level[randomY[i]][randomX[i]].display = ' ' ;
				
					gotoxy(2*randomX[i]+3, randomY[i]+1 ) ;
					cout <<  Level[randomY[i]][randomX[i]+1].display << " " ;
				
					gotoxy(2*randomX[i]+1, randomY[i] +1) ;
					cout << Level[randomY[i]][randomX[i]].display ;
					move = true;
				}
				else
					continue;
			}
			
			
				
		}
		if(move == true)	
			Sleep(500);	
		
}

