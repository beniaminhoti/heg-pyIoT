import machine
from machine import ADC, Pin
from time import sleep
from m5stack import *
import network
import time
import socket

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
# UDP
def udp(donnee):
    """Fontion qui envoie des données à un serveur UDP
    :param donnee: Données à envoyer
    """
    UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPClientSocket.sendto(str(donnee).encode(
        "UTF-8"), ("172.20.10.13", 12345))
################################################################


################################################################
# Light sensor
class Light:
    def __init__(self):
        self.adc = ADC(Pin(35, Pin.IN))  # Fil blanc
        self.adc.atten(ADC.ATTN_11DB)

    def lectAnalogique(self):
        donnees = 0
        for i in range(0, 10):
            lecture = 4095 - self.adc.read()
            donnees += lecture
            return round((100*(donnees)/4096), 0)
################################################################


################################################################
# Main
def main():
    # Création d'une instance de la classe Light
    l = Light()

    # Connection au réseau
    connect()

    # Main loop
    while True:
        print(l.lectAnalogique(), '%')
        udp(l.lectAnalogique())
        sleep(10)
################################################################


if __name__ == '__main__':
    main()
