import paho.mqtt.client as mqtt
import time
import socket

################################################################
# MQTT
def mqtt_publisher(broker_ip, topic):
    """
    Fonction pour publier un message sur un topic d'un broker
    :param broker_ip: str -> Adresse IP du broker
    :param topic: str -> Topic où publier le message
    :param msg: str -> Message à publier
    """
    SERVER_IP = "172.20.10.8"
    PORT_UDP = 12345
    PORT_TCP = 12346
    msg_tcp = tcp_server(SERVER_IP, PORT_TCP)
    msg_udp = udp_server(SERVER_IP, PORT_UDP)

    instance = "Publisher"
    # print(f"Creation de la nouvelle instance: {instance}")
    client = mqtt.Client(instance)

    # print(f"Configuration du mot de passe: sensors")
    client.username_pw_set(username="sensors",password="borandebian")
    # print(f"Connexion au broker: {broker_ip}")
    client.connect(broker_ip)

    print(f"Publication du message: {msg_tcp}")
    client.publish(topic, msg_tcp)

    print(f"Publication du message: {msg_udp}")
    client.publish(topic, msg_udp)
    print()
    # client.publish(topic, "Hello from Publisher")

    # print("Deconnexion du broker")
    # client.disconnect()
################################################################


################################################################
# UDP
def udp_server(server_ip, port):
    """Fonction pour envoyer un message à un serveur UDP

    :param server_ip: str -> Adresse IP du serveur
    :param port: int -> Port du serveur
    :return: str -> Message reçu du client UDP (Light Sensor)
    """
    UDPServerSocket = socket.socket(
        family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Adresse IP de la VM Debian Publisher
    UDPServerSocket.bind((server_ip, port))
    print("Le serveur UDP attend une connexion ...")

    while True:
        msgClient, coordClient = UDPServerSocket.recvfrom(1024)
        print("Le message du Client:", msgClient.decode("UTF-8"))
        print("Adresse IP du client : " + coordClient[0])
        print("Port du client : " + str(coordClient[1]))
        print()
        return msgClient.decode("UTF-8")

    # print("Fin du serveur")
    # UDPServerSocket.close()
################################################################


################################################################
# TCP
def tcp_server(server_ip, port):
    """Fonction pour envoyer un message à un serveur TCP

    :param server_ip: str -> Adresse IP du serveur
    :param port: int -> Port du serveur
    :return: str -> Message reçu du client TCP (Pir Sensor)
    """
    TCPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPServerSocket.bind((server_ip, port))
    TCPServerSocket.listen()
    while True:
        print('Le serveur TCP attend une connexion ...')
        connexion, addr = TCPServerSocket.accept()
        fin = False
        while not fin:
            donnees = connexion.recv(1024).decode("UTF-8")
            if donnees != "":
                print(donnees)
                print()
                connexion.sendall(("reponse: "+donnees).encode('UTF-8'))

            # connexion.close()
            return donnees

    # print("Fin du serveur")
    # TCPServerSocket.close()
################################################################


################################################################
# Main
def main():
    BROKER_IP = "172.20.10.2"  # Debian VM Broker
    TOPIC = "/sensors"

    # Main loop
    while True:
        mqtt_publisher(BROKER_IP, TOPIC)
        time.sleep(2)
################################################################


if __name__ == "__main__":
    main()
