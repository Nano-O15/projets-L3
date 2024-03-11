# Projet - "Méthode de Clustering"

Par OUKHEMANOU Mohand

# DESCRIPTION

Ce projet vise à implémenter différents algorithmes de classification en python afin de comparer les différents résultats obtenus pour répondre à une hypothèse. 
Nous avons choisi une base de données comportant des pingouins appartenant à différentes espèces et vivant sur différentes îles. On possède des données sur la longueur et la profondeur de leur bec, leur masse corporelle et la longueur de leur nageoire.
Le but de notre étude est de déterminer si l'espèce ou l'habitat a une influence sur les caractéristiques physiques de l'animal.

Nous souhaitons alors répondre à deux hypothèses : 
1. L'espèce chez les pingouins influe sur leur caractéristiques physiques. 
2. L'habitat chez les pingouins influe sur leur caractéristiques physiques.  

Pour cela nous avons décidé d'implémenter l'algorithme K-Means, l'algorithme GMM (ou Gaus- sian Mixture Model), l'algorithme Mean-Shift, l'algorithme DBSCAN et l'algorithme CAH. 
Dans ce but, nous utilisons les bibliothèques `sklearn` et `scipy`, et pour l'affichage des résultats nous utilisons les bibliothèques `matplotlib` et `seaborn`.

Les résultats & conclusion détaillés de notre étude se trouvent dans le rapport présent dans ce dossier.

# PRÉ-REQUIS

Avant de commencer, assurez-vous d'avoir Python installé sur votre machine, ainsi que les bibliothèques pandas, seaborn, matplotlib, scipy & sklearn. 
Voici les étapes pour l'installation :
    Installer Python : https://www.python.org/downloads/
    Installer pandas : pip/pip3 install pandas
    Installer seaborn : pip/pip3 install seaborn
    Installer matplotlib : pip/pip3 install matplotlib
    Installer scipy : pip/pip3 install scipy
    Installer sklearn : pip/pip3 install sklearn
    
# **UTILISATION**

Pour lancer le programme, placez-vous dans le dossier de l'algorithme voulu & exécutez le en utilisant :
    -> python/python3 nom_du_fichier.py

Chaque programme affiche les différents graphes de dispersion, en fonction de l'espèce et en fonction de l'île, puis la dispersion du clustering. 
Aussi, s'il ya des méthodes d'analyse qualitative du clustering, les courbes sont également affichées.