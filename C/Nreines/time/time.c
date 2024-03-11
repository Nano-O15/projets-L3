/* Algorithmique Avancée */
/* OUKHEMANOU Mohand L3-A */
/* Projet */

#include <stdio.h>
#include <stdlib.h>
#include "fonctions.h"
#include <time.h>

int main()
{
    // On instancie nos variables.
    board b;

    int i, j, n, s;

    clock_t td, ta, dt;

    // La boucle pour mesurer le temps d'exécution de notre programme, à différentes valeurs de n.
    for (n = 1; n < 16; n++)
    {
        printf("n : %d\t\n", n);

        // clock() renvoie le nombre de "ticks" consommé par le programme en cours d'exécution (ce qui correspond au temps d'exécution) avant l'appel des fonctions dans la boucle. 
        td = clock();
        for (int i = 0; i < n; i++)
        {
            b.n = n;

            b.game = (char **)malloc(b.n * sizeof(int *));

            for (i = 0; i < b.n; ++i)
            {
                b.game[i] = (char *)malloc(b.n * sizeof(int));
            }

            for (i = 0; i < b.n; i++)
            {
                for (j = 0; j < b.n; j++)
                {
                    b.game[i][j] = '.';
                }
            }

            s = solve(b, 0);

            printf("Nombre total de solutions : %d\n", s);

            for (i = 0; i < b.n; ++i)
            {
                free(b.game[i]);
            }

            free(b.game);
        }
        // clock() renvoit le nombre de "ticks" consommé par le programme en cours d'exécution (ce qui correspond au temps d'exécution) après l'appelle des fonctions dans la boucle. 
        ta = clock();
        // On affiche le temps d'exécution, obtenu avec la soustraction du temps après appel des fonctions et du temps avant appel des fonctions.
        printf("Time : %ld\t", (int)ta - td);

        printf("\n\n");
    }

    return 0;
}