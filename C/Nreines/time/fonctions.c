/* Algorithmique Avancée */
/* OUKHEMANOU Mohand L3-A */
/* Projet */

#include <stdio.h>
#include <stdlib.h>
#include "fonctions.h"

void display(board b)
{
    int i, j;

    printf("Solution :\n\n\n");

    // On affiche chaque case du plateau de jeu.
    for (i = 0; i < b.n; i++)
    {
        for (j = 0; j <= b.n; j++)
        {
            printf("%6c", b.game[i][j]);
        }

        printf("\n\n");
    }

    printf("\n");
}

void print_solutions(board b)
{
    printf("Solution : {ligne, colonne}\n\n");

    // On affiche la paire de positions de chaque reine rencontrée.
    for (int x = 0; x < b.n; x++)
    {
        for (int y = 0; y < b.n; y++)
        {
            if (b.game[x][y] == 'R')
            {
                printf("{%d, %d} ", x, y);
            }
        }
    }

    printf("\n\n");
}

char check(board b, int x, int y)
{
    // On vérifie le contenu des cases du dessus dans la colonne.
    for (int i = 0; i < x; i++)
    {
        if (b.game[i][y] == 'R')
        {
            return '.';
        }
    }

    // On vérifie le contenu des cases dans la diagonale haut-gauche.
    for (int i = x, j = y; (i >= 0) && (j >= 0); i--, j--)
    {
        if (b.game[i][j] == 'R')
        {
            return '.';
        }
    }

    // On vérifie le contenu des cases dans la diagonale haut-droite.
    for (int i = x, j = y; (i >= 0) && (j < b.n); i--, j++)
    {
        if (b.game[i][j] == 'R')
        {
            return '.';
        }
    }

    return 'R';
}

char *next_moves(board b, int x, char *possible)
{
    // On ajoute à notre tableau de char, le retour de la fonction check() pour x la ligne qui nous intéresse et avec y = la variable i (on étudie toutes les cases de la ligne x). 
    for (int i = 0; i < b.n; i++)
    {
        // On enregistre le retour de check() à l'index i, avec i la colonne étudiée.
        possible[i] = check(b, x, i);
    }

    return possible;
}

int solve(board b, int x)
{
    int nb_s = 0;
    char *possible;

    // On alloue dynamiquement l'espace pour notre tableau de choix possibles.
    possible = (char *)malloc(b.n * sizeof(*possible));

    // Condition de sortie, qui renvoie 1 si on remplit chaque ligne du plateau (ce qui correspond à une solution viable au problème).
    if (x >= b.n)
    {
        return 1;
    }

    // On remplit notre tableau de char avec les choix possibles pour la ligne x.
    possible = next_moves(b, x, possible);

    for (int i = 0; i < b.n; i++)
    {
        // Dès que l'on rencontre un choix viable :
        if (possible[i] == 'R')
        {
            // On place ce choix.
            b.game[x][i] = 'R';
            // On appelle récursivement notre fonction solve() en passant à la ligne suivante (x+1).
            nb_s += solve(b, x + 1);
            // Une fois toutes les solutions dépendant de ce choix évalué, on supprime ce placement du plateau de jeu. 
            b.game[x][i] = '.';
        }
    }

    // On libère la mémoire allouée à notre tableau de choix possibles. 
    free(possible);

    return nb_s;
}