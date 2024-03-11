import socket
import sys
from time import sleep

from Crypto.Util.number import getPrime, inverse
import hashlib


def gen_rsa_keypair(bits):
    pq_size = bits // 2  # 2).
    p = getPrime(pq_size)
    q = getPrime(pq_size)
    assert(p != q)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = 65537
    assert(e < phi_n and phi_n % e != 0)
    d = inverse(e, phi_n)
    return ((e, n), (d, n))


def expo_modulaire(x, y, z):
    res = 1
    while (y > 0):
        if ((y & 1) > 0):
            res = (res * x) % z
        y >>= 1
        x = (x * x) % z
    return res


def rsa(msg, key):
    e_mod = expo_modulaire(msg, key[0], key[1])
    return e_mod


def rsa_enc(msg, key):
    i_msg = int.from_bytes(msg.encode('utf-8'), 'big')
    if (i_msg > key[1]):
        return "Le message doit être strictement inferieur à n."
    return rsa(i_msg, key)


def rsa_dec(msg, key):
    if (msg > key[1]):
        return "Le chiffre doit être strictement inferieur à n."
    c_msg = rsa(msg, key)
    s_msg = c_msg.to_bytes((c_msg.bit_length() + 7) //
                           8, 'big').decode('utf-8')
    return s_msg


def h(msg):
    h_msg = int.from_bytes(hashlib.sha256(
        bytes(str(msg), encoding='utf-8')).digest(), "big")
    return h_msg


def rsa_sign(msg, key):
    sg_msg = rsa(h(msg), key)
    return (msg, sg_msg)


def rsa_verify(msg, key):
    v_msg = rsa(msg[1], key)
    if (h(msg[0]) == v_msg):
        return True
    return False


HOST = '127.0.0.1'
PORT = 8080


def serveur():
    # On génère une clé rsa au serveur.
    s_key = gen_rsa_keypair(1024)

    # On créer un tuple public_key pour la clé public du client.
    c_key = (0, 0)
    list_c_key = list(c_key)

    # Étape 1: Créer la socket TCP du serveur.
    # AF_INET est la verion du protocole IP utilisé (ici IPv4).
    # SOCK_STREAM est le protocole de transport utilisé (pour le protocole TCP).
    serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # On traite les erreurs.
    if (serv_socket == -1):
        print("La création de la socket a échouée !\n")
        sys.exit()

    else:
        print("La socket a été créée avec succès !\n")

    # Étape 2 : Associer la socket à une adresse IP et un numéro de port TCP, via la fonction bind(adress, port).
    # SERVER_LOCALHOST est notre adresse IP et PORT est le port que l'on va utiliser.
    serv_socket.bind((HOST, PORT))
    print("L'adresse a été associée à la socket !\n")

    # Étape 3 : Configurer le nombre de connexion que pourra prendre en charge notre serveur, via la fonction socket.listen(n).
    # n étant le nombre maximal de connexions pouvant être prise en charge simultanément.
    serv_socket.listen(2)

    if (serv_socket.listen(2) == -1):
        print("Erreur lors de la configuration !\n")
        sys.exit()

    # Étape 4 : Obtention d'un canal de communication par l'application, via la fonction accept().
    socket_connect, address = serv_socket.accept()

    if (socket_connect == -1):
        print("Erreur de connexion !\n")
        sys.exit()

    else:
        print("Nouvelle connexion depuis : " + str(address))

    # On récupère le pseudo de l'utilisateur du client.
    user = socket_connect.recv(1024).decode()

    # On récupère la clé publique du client.
    list_c_key[0] = int(socket_connect.recv(1024).decode())
    sleep(1)
    list_c_key[1] = int(socket_connect.recv(1024).decode())
    print("\nClé Publique Reçu !\n")
    c_key = tuple(list_c_key)
    sleep(1)

    # On va envoyer la clé publique du serveur.
    socket_connect.send(str(s_key[0][0]).encode())
    sleep(1)
    socket_connect.send(str(s_key[0][1]).encode())
    print("Clé Publique Envoyé !\n")

    while(1):
        #  On reçoit le message du client avec la fonction recv(bufsize[, flags].decode()).
        # bufsize[, flags] étant le nombre de bits à récevoir (au maximum) et flags étant les valeurs supporté par l'OS.
        # On utilise également la fonction decode() pour décoder le message reçu encodé via le codec enregistré pour l'encodage, il utilise par défaut l'encodage de string.
        message_r = int(socket_connect.recv(1024).decode())
        sleep(1)
        message_rs = int(socket_connect.recv(1024).decode())

        verif_tuple = (message_r, message_rs)

        if (rsa_verify(verif_tuple, c_key) == True):
            print("\nMessage Authentique !")
            message_rd = rsa_dec(int(message_r), s_key[1])
            print(user + " : " + str(message_rd))

        # Si le message reçu est "Bye !", on ferme le chat.
        if (message_rd == "Bye !"):
            print(user + " a quitté.\n")
            break

        message_e = input('\nVotre message : ')

        # On va chiffrer le message que l'on veux envoyer.
        message_ec = rsa_sign(rsa_enc(message_e, c_key), s_key[1])

        # On envoie le message depuis le serveur en utilisant la fonction send(bytes[, flags]).
        # bufsize[, flags] étant le nombre de bits à envoyer (au maximum) et flags étant les valeurs supporté par l'OS (comme précédemment).
        # On utilise également la fonction encode() pour encodé notre message, il utilise par défaut l'encodage de string.
        socket_connect.send(str(message_ec[0]).encode())
        sleep(1)
        socket_connect.send(str(message_ec[1]).encode())

        # Si le message tapé est "Bye !", on ferme le chat.
        if (message_ec == rsa_sign(rsa_enc("Bye !", c_key), s_key[1])):
            print("Le serveur a quitté.\n")
            break

    # Fermeture de la socket, via la fonction close().
    socket_connect.close()


if __name__ == '__main__':
    serveur()
