from realudp import *
from time import *
from gpio import *

def onUDPReceive(ip, port, data):
	
	### UDP to Hall ###
	IP = "172.20.10.5" #Adresse IP du M5Stack Hall
	PORT = 24345
	socket = RealUDPSocket()
	###################
	
	### Sensors ###
	LED_INPUT = 0
	LCD_INPUT = 1
	pinMode(LED_INPUT, OUT)
	pinMode(LCD_INPUT, OUT)
	###############
	
	print("Received from " + ip + ":" + str(port) + ": " + data)
	
	if(data == '0'):
			customWrite(LCD_INPUT, '')
			digitalWrite(LED_INPUT, 0)
			socket.send(IP, PORT, data)
	else:
			customWrite(LCD_INPUT, 'Hello')
			digitalWrite(LED_INPUT, 1023)
			socket.send(IP, PORT, data)
	

def main():
	IP_BIND = "172.20.10.8" #Adresse IP du MackBook
	PORT_BIND = 12345

	socket = RealUDPSocket()
	socket.onReceive(onUDPReceive)
	print(socket.begin(PORT_BIND))

	# don't let it finish
	while True:
		sleep(2)

if __name__ == "__main__":
	main()
	