# Projet - "Résolution du problème des N-Reines"

Par OUKHEMANOU Mohand

# DESCRIPTION

## OBJECTIF DU PROJET

Le but du problème des N-Reines est de placer n reines (d’un jeu d’échecs), sur un plateau de n*n cases, le tout en respectant les règles des échecs.
Soit, que les reines ne se menacent pas mutuellement (qu’elles ne soient pas sur la même ligne, la même colonne ou la même diagonale), une solution est possible pour chaque entier naturel, excepté 2 et 3.
Aujourd’hui on a pu résoudre le problème jusqu’à 27 reines, avec un total de 234,907,967,154,122,528 solutions possibles (sur le principe de symétrie).
Le but de ce projet est d'implémenter un algorithme afin de résoudre ce problème pour un n donné par l'utilisateur. 

## APPROCHE DE RÉSOLUTION

Ici, on utilise le backtracking via la récursivité, afin de pouvoir tester chaque "chemin de l’arbre de résolution" (à voir comme un arbre où chaque nœud est une position sur la ligne), et à chaque fois qu’une suite de n positions respecte la règle, on l’ajoute à un vecteur de position.
Le programme affichera alors toutes les configurations valides trouvées pour le nombre donné de reines.

Le programme dans le dossier "time" permet de renvoyer le temps d'exécution du programme pour chaque n et de stocker les résultats dans un fichier ("time.txt"). Cela permet de visualiser l'efficacité de notre algorithme et éventuellement d'utiliser ces résultats pour comparer avec d'autres algorithmes.
À partir d'un certain n, le temps d'exécution devient très long, il suffit alors d'utiliser les touches "ctrl+z" pour le quitter. 

# **UTILISATION**

Pour lancer le programme, suivez ces étapes :
    1. Compiler le code en exécutant la commande : make.
    2. Exécuter l'algorithme en lançant : 
        -> ./nreines
        -> spécifier le nombre de reines (n) comme argument en ligne de commande. 

Pour le programme dans "time", l'utilisation est la même, à la différence qu'il ne sera pas nécessaire de spécifier le nombre de reines. 