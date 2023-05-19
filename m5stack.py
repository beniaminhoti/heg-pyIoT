import machine
from machine import ADC, Pin
from time import sleep
from m5stack import *
import network
import socket
import time

AUTH_OPEN = 0
AUTH_WEP = 1
AUTH_WPA_PSK = 2
AUTH_WPA2_PSK = 3
AUTH_WPA_WPA2_PSK = 4

SSID = "iPhone de Boran"
PASSWORD = "borancowifi"

def do_connect(ssid,psw):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    s = wlan.config("mac")
    mac = ('%02x:%02x:%02x:%02x:%02x:%02x').upper() %(s[0],s[1],s[2],s[3],s[4],s[5])
    print("Local MAC:"+mac) #get mac 
    wlan.connect(ssid, psw)
    if not wlan.isconnected():
        print('Connexion au reseau: ' + ssid)
        wlan.connect(ssid, psw)
 
    start = time.ticks_ms() # get millisecond counter
    while not wlan.isconnected():
        time.sleep(1) # sleep for 1 second
        if time.ticks_ms()-start > 20000:
            print("Timeout de connexion!")
            break
 
    if wlan.isconnected():
        print('Adresses IP: ', wlan.ifconfig())
    return wlan
 
def connect():
 do_connect(SSID,PASSWORD)

class Light:
    def __init__(self):
        self.adc = ADC(Pin(35,Pin.IN)) # Fil blanc
        self.adc.atten(ADC.ATTN_11DB)
        
    def lectAnalogique(self):
        donnees = 0
        for i in range(0, 10):
            lecture = 4095 - self.adc.read()
            donnees += lecture
            return round((100*(donnees)/4096), 0)
def main():
    connect()
    l=Light()
    clientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        print(l.lectAnalogique(),'%')
        clientUDP.sendto(str(l.lectAnalogique()).encode("UTF-8"), ("172.20.10.8", 12345))
        time.sleep(1)

main()




