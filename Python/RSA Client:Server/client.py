import socket
import sys

from Crypto.Util.number import getPrime, inverse
import hashlib

from time import sleep


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


def client():
    #On demande à l'utilisateur son pseudo.
    pseudo = input('Quel est votre pseudo ? : ')

    # On génère une clé rsa au client.
    c_key = gen_rsa_keypair(1024)

    # On créer un tuple public_key pour la clé publique du serveur.
    s_key = (0, 0)
    list_s_key = list(s_key)

    # Étape 1: Créer la socket TCP du client.
    # AF_INET est la verion du protocole IP utilisé (ici IPv4).
    # SOCK_STREAM est le protocole de transport utilisé (pour le protocole TCP).

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # On traite les erreurs.
    if (client_socket == -1):
        print("La création de la socket a échouée !\n")
        sys.exit()

    else:
        print("\nLa socket a été créée avec succès !\n")

    # Étape 2 : On connecte le client au serveur, via la fonction connect(adress).
    # adress étant les informations de connexion du serveur (son adresse IP et son port).
    client_socket.connect((HOST, PORT))

    # On va envoyer le pseudo de l'utilisateur du client.
    client_socket.send(pseudo.encode())
    sleep(1)

    # On va envoyer la clé publique du client.
    client_socket.send(str(c_key[0][0]).encode())
    sleep(1)
    client_socket.send(str(c_key[0][1]).encode())
    print("Clé Publique Envoyé !\n")
    sleep(1)

    # On récupère la clé publique du serveur.
    list_s_key[0] = int(client_socket.recv(1024).decode())
    sleep(1)
    list_s_key[1] = int(client_socket.recv(1024).decode())
    print("Clé Publique Reçu !\n")
    s_key = tuple(list_s_key)

    message_e = input('Votre message : ')

    while(1):
        # On va chiffrer le message que l'on veux envoyer.
        message_ec = rsa_sign(rsa_enc(message_e, s_key), c_key[1])

        # On envoie le message depuis le client en utilisant la fonction send(bytes[, flags]).
        # bufsize[, flags] étant le nombre de bits à envoyer (au maximum) et flags étant les valeurs supporté par l'OS.
        # On utilise également la fonction encode() pour encodé notre message, il utilise par défaut l'encodage de string.
        client_socket.send(str(message_ec[0]).encode())
        sleep(1)
        client_socket.send(str(message_ec[1]).encode())

        # Si le message tapé est "Bye !", on ferme le chat.
        if (message_ec == rsa_sign(rsa_enc("Bye !", s_key), c_key[1])):
            print(pseudo + " a quitté.\n")
            break

        # On reçoit le message du serveur avec la fonction recv(bufsize[, flags].decode()).
        # bufsize[, flags] étant le nombre de bits à récevoir (au maximum) et flags étant les valeurs supporté par l'OS.
        # On utilise également la fonction decode() pour décoder le message reçu encodé via le codec enregistré pour l'encodage, il utilise par défaut l'encodage de string.
        message_r = int(client_socket.recv(1024).decode())
        sleep(1)
        message_rs = int(client_socket.recv(1024).decode())

        verif_tuple = (message_r, message_rs)

        if (rsa_verify(verif_tuple, s_key) == True):
            print("\nMessage Authentique !")
            message_rd = rsa_dec(int(message_r), c_key[1])
            print("Serveur : " + str(message_rd))

        # Si le message reçu est "Bye !", on ferme le chat.
        if (message_rd == "Bye !"):
            print("Le serveur a quitté.\n")
            break

        message_e = input('\nVotre message : ')

    # Fermeture de la socket, via la fonction close().
    client_socket.close()


if __name__ == '__main__':
    client()
