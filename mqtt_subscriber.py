import paho.mqtt.client as mqtt
import socket

################################################################
# UDP
def udp_send(udp_serv_ip, port, msg):
    """ 
    Fonction pour envoyer un message à un serveur UDP (Packet Tracer)
    :param udp_serv_ip: str -> Adresse IP du serveur UDP (IP du MacBook)
    :param port: int -> Port du serveur UDP
    :param msg: str -> Message à envoyer
    """
    UDPClientSocket = socket.socket(
        family=socket.AF_INET, type=socket.SOCK_DGRAM)
    print("---- Message envoyé ----")
    print("Message envoyé: ", msg)
    print("------------------------\n")
    UDPClientSocket.sendto(msg.encode('UTF-8'), (udp_serv_ip, port))
    UDPClientSocket.settimeout(2)
################################################################


################################################################
# MQTT
def on_message(client, userdata, message):
    """ 
    Function to publish a message to a broker on a topic
    :param client: mqtt.Client -> Client instance that received the message
    :param userdata: Any -> User defined data
    :param message: mqtt.MQTTMessage -> Message received
    :return: str -> Message received
    """
    msg = str(message.payload.decode("utf-8"))
    print("---- Message reçu ----")
    print("Message received: ", msg)
    print("Message topic: ", message.topic)
    print("Message qos: ", message.qos)
    print("Message retain flag: ", message.retain)
    print("----------------------\n")
    PORT = 12345
    UDP_SERV_IP = "172.20.10.8"  # Adresse IP du MacBook -> (Packet Tracer)
    udp_send(UDP_SERV_IP, PORT, msg)


def mqtt_sub(broker_ip, topic):
    """
    Fonction pour s'abonner à un topic MQTT
    :param broker_ip: str -> IP address of the broker
    :param topic: str -> Topic to subscribe to
    """
    instance = "Subscriber"
    print(f"Creation de la nouvelle instance: {instance}")
    client = mqtt.Client(instance)
    client.on_message = on_message
    print(client.on_message)

    print(f"Configuration du mot de passe: sensors")
    client.username_pw_set(username="sensors",password="borandebian")
    
    print(f"Connexion au broker: {broker_ip}")
    client.connect(broker_ip)

    client.loop_start()  # Démarrage de la boucle
    print(f"Inscription au topic: {topic}")
    client.subscribe(topic)
    print()

    while True:
        pass
    client.loop_stop()
################################################################


################################################################
# Main
def main():
    BROKER_IP = "172.20.10.2"
    TOPIC = "/sensors"
    mqtt_sub(BROKER_IP, TOPIC)
################################################################

if __name__ == "__main__":
    main()