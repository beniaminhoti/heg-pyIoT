from machine import Pin
import socket
import network
import time
from m5stack import *
import urequests as requests

################################################################
# Network
AUTH_OPEN = 0
AUTH_WEP = 1
AUTH_WPA_PSK = 2
AUTH_WPA2_PSK = 3
AUTH_WPA_WPA2_PSK = 4

SSID = "iPhone de Boran"
PASSWORD = "borancowifi"


def do_connect(ssid, psw):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    s = wlan.config("mac")
    mac = ('%02x:%02x:%02x:%02x:%02x:%02x').upper() % (
        s[0], s[1], s[2], s[3], s[4], s[5])
    print("Local MAC: "+mac)  # get mac
    wlan.connect(ssid, psw)
    if not wlan.isconnected():
        print('Connexion au reseau: ' + ssid)
        wlan.connect(ssid, psw)

    start = time.ticks_ms()  # get millisecond counter
    while not wlan.isconnected():
        time.sleep(1)  # sleep for 1 second
        if time.ticks_ms()-start > 20000:
            print("Timeout de connexion!")
            break

    if wlan.isconnected():
        print('Adresses IP: ', wlan.ifconfig())
    return wlan


def connect():
    do_connect(SSID, PASSWORD)
################################################################


################################################################
# Hall sensor
class Hall():
    def __init__(self):
        self.pin = Pin(22, Pin.IN)
        self.pin.irq(trigger=(Pin.IRQ_RISING | Pin.IRQ_FALLING),
                     handler=self.actionInterruption)

    def actionInterruption(self, pin):
        val = 0
        if (pin.value() == 1):
            print("Magnet disconnected")  # Si les volets sont ouverts
            val = 1
        else:
            print("Magnet connected")  # Si les volets sont fermés
            val = 0
        return val
################################################################


################################################################
# UDP
def udp_server():
    """Fonction 'main'. Elle permet de recevoir les messages du client, 
       fait des conditions et envoie des notifications sur telegram.
    """
    # Telegram
    TOKEN = '' # Token du bot Telegram (à remplir)
    chat_id = ''  # Boran - ID du chat (à remplir)
    chat_id_2 = ''  # Sara - ID du chat (à remplir)

    UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPServerSocket.bind(("172.20.10.5", 56345))
    print("The UDP server is waiting for a connection..")

    # Création d'une instance de la classe Hall
    h = Hall()

    while True:
        msg_client, coord_client = UDPServerSocket.recvfrom(1024)
        received_message = msg_client.decode("UTF-8")
        print(received_message)

        if received_message == '1' or h.actionInterruption == 1:
            print("Magnet connected")

        else:
            print("Magnet disconnected")
            send_notification(TOKEN, chat_id, "Fermez les volets")
            send_notification(TOKEN, chat_id_2, "Fermez les volets")

    UDPServerSocket.close()
################################################################


################################################################
# Telegram
def send_notification(token, chat_id, message):
    """Fonction permettant d'envoyer une notification Telegram.
    :param token: str -> API Key du bot Telegram
    :param chat_id: str -> ID du chat
    :param message: str -> Message à envoyer
    """
    try:
        url = "https://api.telegram.org/bot{}/sendMessage".format(token)
        payload = {
            "chat_id": chat_id,
            "text": message
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Notification sent successfully.")
        else:
            print("Error sending notification:", response.text)
    except Exception as e:
        print("Error sending notification:", str(e))
################################################################


################################################################
# Main
def main():
    connect()
    udp_server()
################################################################


if __name__ == "__main__":
    main()
