from tcp import *
from time import *
from realudp import *


"""
def onTCPConnectionChange(type):
	print("Connection to " + client.remoteIP() + " changed to state " + str(type))

def onTCPReceive(data):
	print("Received from " + client.remoteIP() + " with data: " + data)
"""

def onUDPReceive(ip, port, data):
	print("Received from "
		+ ip + ":" + str(port) + ": " + data);
	return data #comment recup data ???

def main():
	### UDP ###
	IP = "172.20.10.8"
	PORT = 12345
	
	socket = RealUDPSocket()
	socket.onReceive(onUDPReceive)
	print("\nConnexion UDP")
	print(socket.begin(PORT))
	print('')
	###     ###

	### TCP ###
	serverIP = "192.168.25.100" #SBC0
	serverPort = 55997
	client = TCPClient()
	print("\nConnexion TCP")
	print(client.connect(serverIP, serverPort))
	print('')
	###     ###
	
	
	"""
	client.onConnectionChange(onTCPConnectionChange)
	client.onReceive(onTCPReceive)
	"""
	

	while True:
		#print(data)
		client.send("sent from SBC1 manually")
		sleep(1)

if __name__ == "__main__":
	main()
	