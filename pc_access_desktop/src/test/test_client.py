import socket
from src.constants import *


def client_to_test_tcp(ips=["192.168.1.8"]):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ips[0], 42424))
    client.send("Ola mundo|".encode())
    client.send("Ola novo mundo|".encode())
    client.send("Ola mundo imundo|".encode())
    client.send(AppConnection.PCA_DISCONNECT.encode())

    client.close()


def client_to_test_udp():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address = ('192.168.1.7', 24242)
    msg = b'testando socket UDP msg do cliente'
    client.sendto(msg, address)


if __name__ == '__main__':
    client_to_test_tcp()
    client_to_test_udp()