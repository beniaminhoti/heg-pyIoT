import machine
from machine import ADC, Pin
from time import sleep
from m5stack import *

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
        
l=Light()
while True:
    print(l.lectAnalogique(),'%')
    lcd.print(l.lectAnalogique(),'%')
    sleep(1)