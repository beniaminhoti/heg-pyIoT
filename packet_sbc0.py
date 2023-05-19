from tcp import *
from time import *
from gpio import *


def onTCPNewClient(client):
	def onTCPConnectionChange(type):
		print("connection to " + client.remoteIP() + " changed to state " + str(type))
		
	def onTCPReceive(data):
		print("Received from " + client.remoteIP() + " with data: " + data)
		# send back same data
		# client.send(data)

	client.onConnectionChange(onTCPConnectionChange)
	client.onReceive(onTCPReceive)

def main():
	
	### Sensors ###
	LED_INPUT = 0
	LCD_INPUT = 1
	pinMode(LED_INPUT, OUT)
	pinMode(LCD_INPUT, OUT)
	###         ###
	
	### TCP ###
	port = 55997
	server = TCPServer()
	server.onNewClient(onTCPNewClient)
	print(server.listen(port))
	###     ###

	# don't let it finish
	while True:
		data = 0 #Received data from SBC1
		if(data == 0):
			customWrite(LCD_INPUT, '')
			digitalWrite(LED_INPUT, 0)
		else:
			customWrite(LCD_INPUT, 'Hello')
			digitalWrite(LED_INPUT, 1023)
		sleep(3600)

if __name__ == "__main__":
	main()