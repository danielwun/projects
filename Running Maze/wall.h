#ifndef CELL_H
#define CELL_H
struct Cell
{
	bool visited ;
	bool top_wall ;
	bool bot_wall ;
	bool left_wall ;
	bool right_wall ;
	char display ;
	int life ;
};
#endif
