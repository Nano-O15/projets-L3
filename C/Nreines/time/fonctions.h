/* Algorithmique Avancée */
/* OUKHEMANOU Mohand L3-A */
/* Projet */

#ifndef _N_REINES
#define _N_REINES

typedef struct board
{
    int n;
    char **game;
} board;

void display(board b);
void print_solutions(board b);
char check(board b, int x, int y);
char* next_moves(board b, int x, char*possible);
int solve(board b, int x);

#endif