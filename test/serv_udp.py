import sys
import socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((sys.argv[1], 12345)) # sys.argv[1] = adresse IP du serveur
print("Le serveur UDP attend un connexion ...")

fin = False
while not fin:
    msgClient, coordClient = UDPServerSocket.recvfrom(1024)
    if msgClient.decode("UTF-8") == "FIN":
        fin = True
    else:
        print("Le message du Client:", msgClient.decode("UTF-8"))
        print("adresse IP du client : " + coordClient[0])
        print("port du client : " + str(coordClient[1]))

        UDPServerSocket.sendto(
            f"Bonjour {coordClient[0]}, signé le serveur".encode("UTF-8"), coordClient)

print("Fin du serveur")
UDPServerSocket.close()
