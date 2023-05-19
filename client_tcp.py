import socket
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(("172.20.10.8", 12346))
print ("Connexion ouverte")
for i in range(1,5):
 print ("Envoi "+str(i))
 socket.sendall(str(i).encode("UTF-8"))
 print(socket.recv(1024).decode("UTF-8"))
socket.send(b"")
print("Fermeture connexion")
socket.close() 