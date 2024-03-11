# Projet - "Envoi de données chiffrées par la méthode RSA - Client/Server"

Par OUKHEMANOU Mohand

# DESCRIPTION

Ce projet vise à mettre en place un système de communication sécurisée en utilisant le chiffrement RSA et la programmation par sockets. La programmation socket permet la communication entre plusieurs processus, que ce soit sur la même machine ou à travers le réseau.

Pour ce projet, le protocole choisi est le TCP (Transmission Control Protocol), largement utilisé dans la programmation de sockets. Il se compose de trois étapes : l'établissement de la connexion, le transfert des données et la fermeture de la connexion. Deux étapes supplémentaires ont été ajoutées : l'envoi du pseudonyme de l'utilisateur du client et l'échange des clés publiques entre le serveur et le client.

# PRÉ-REQUIS

Avant de commencer, assurez-vous d'avoir Python installé sur votre machine, ainsi que la bibliothèque crypto. 
Voici les étapes pour l'installation :
    Installer Python : https://www.python.org/downloads/
    Installer crypto : pip/pip3 install pycryptodome
    
# **UTILISATION**

Pour lancer le programme, exécutez les commandes suivantes dans deux terminals différents :
    -> python/python3 client.py pour lancer l'instance du client.
    -> python/python3 serveur.py pour lancer l'instance du serveur.

Lors du lancement du client, l'utilisateur est invité à entrer son pseudonyme. 
Ensuite, la connexion est établie, où chacun envoie sa clé publique. Une fois que cela est fait, le client peut envoyer son premier message. 
Le serveur le recevra, vérifiera son intégrité et le déchiffrera avant d'envoyer sa réponse. Pour quitter la conversation, il suffit d'envoyer le message "Bye !".