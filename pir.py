from time import sleep
from machine import Pin
from m5stack import *
import network
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

# 172.20.10.4


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
# Pir sensor
class Pir():
    def __init__(self):
        self.pin = Pin(22, Pin.IN)
        self.mvt = 0
        self.pin.irq(trigger=(Pin.IRQ_RISING | Pin.IRQ_FALLING),
                     handler=self.actionInterruption)

    def actionInterruption(self, pin):
        if (pin.value() == 1):
            print("1")
            self.mvt = 1
        else:
            print("0")
            self.mvt = 0
################################################################


################################################################
# TCP
def tcp(donnee):
    try:
        TCPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCPClientSocket.connect(("172.20.10.13", 12346))
        TCPClientSocket.send(str(donnee).encode("UTF-8"))
        TCPClientSocket.close()
    except OSError as e:
        print("TCP Error:", e)
################################################################


################################################################
def main():
    # Création d'une instance de la classe Pir
    pir = Pir()

    # Connexion au réseau
    connect()

    # Main loop
    while True:
        # Si le capteur détecte un mouvement
        if pir.mvt == 1:
            print("1")
            tcp("1")
        else:
            print("0")
            tcp("0")
        sleep(10)
################################################################


if __name__ == '__main__':
    main()
