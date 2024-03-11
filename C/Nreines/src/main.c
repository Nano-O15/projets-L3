/* Algorithmique Avancée */
/* OUKHEMANOU Mohand L3-A */
/* Projet */

#include <stdio.h>
#include <stdlib.h>
#include "../headers/fonctions.h"

int main()
{
    // On instancie nos variables.
    board b;

    int i, j, u_n, s;

    // On demande à l'utilisateur le n désiré pour le jeu.
    printf("Quel est votre n ? ");
    scanf("%d", &u_n);
    printf("\n");

    while (u_n == 0)
    {
        printf("Veuillez choisir un n supérieur ou égal à 1 !\n");
        printf("Quel est votre n ? ");
        scanf("%d", &u_n);
        printf("\n");
    }

    // On attribue le n choisit par l'utilisateur au n du board.
    b.n = u_n;

    // On alloue dynamiquement l'espace pour notre plateau de jeu (tableau à deux dimensions).
    b.game = (char **)malloc(b.n * sizeof(int *));

    for (i = 0; i < b.n; ++i)
    {
        b.game[i] = (char *)malloc(b.n * sizeof(int));
    }

    // On remplit le plateau par des cases vides (représenté par un '.').
    for (i = 0; i < b.n; i++)
    {
        for (j = 0; j < b.n; j++)
        {
            b.game[i][j] = '.';
        }
    }

    // On attribue à la variable s, la valeur renvoyée par la fonction solve(), soit le nombre total de solutions.
    s = solve(b, 0);

    // En fonction de cette valeur on affiche une phrase différente.
    if (s == 0)
    {
        printf("Aucune solution possible !\n");
    }

    else
    {
        printf("Nombre total de solutions : %d\n", s);
    }

    // On libère la mémoire allouée à notre plateau de jeu (tableau à deux dimensions).
    for (i = 0; i < b.n; i++)
    {
        free(b.game[i]);
    }

    free(b.game);

    return 0;
}