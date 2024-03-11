# Projet - "Web Scrapper"

Par OUKHEMANOU Mohand

# DESCRIPTION

Ce projet vise à développer un outil de scraping pour extraire des données textuelles d'un site web en se concentrant sur un thème spécifique pour former un corpus. Dans ce cas, le thème choisi est Pokémon. L'objectif principal est de créer un Pokédex des quatre premières générations, en construisant une base de données contenant des informations sur les Pokémon.

Nous avons utilisé le site poképédia.fr comme source de données et les bibliothèques BeautifulSoup et Requests pour le scraping. Les bibliothèques Pandas et CSV ont été employées pour la gestion de la base de données, tandis que les bibliothèques Functools et Operator ont facilité la manipulation des listes. Enfin, la bibliothèque Re(gex) a été utilisée pour le traitement des données textuelles.

# PRÉ-REQUIS

Avant de commencer, assurez-vous d'avoir Python installé sur votre machine, ainsi que la bibliothèque beautifulsoup. 
Voici les étapes pour l'installation :
    Installer Python : https://www.python.org/downloads/
    Installer beautifulsoup : pip/pip3 install bs4  
    
# **UTILISATION**

Pour lancer le programme, exécutez la commande suivante :
    -> python/python3 web_scraping.py
Veuillez noter que le processus peut prendre environ 5 minutes pour s'exécuter, car il y a 493 pages à scraper. Une fois exécuté, le programme va extraire les données de chaque page et les sauvegarder à la fois dans un fichier CSV et dans un tableur (fichier XLSX).

ATTENTION : le projet servant à scrapper des données d'une page web, si cette dernière est modifiée, le code pourrait ne plus être viable. Il faudrait alors réadapter ce code à la nouvelle structure de la page. 