import socket
import sys

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.sendto(sys.argv[1].encode(  # sys.argv[1] est le message à envoyer
    "UTF-8"), ("172.20.10.8", 12345))
