from mpu6050 import mpu6050
import socket
from time import sleep          #import

connected = False

def udp_send(msg, addr=""):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
	msg = msg.encode("utf-8")
	sock.sendto(msg, addr)


def wait_connect():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(("", 22444))
	while(True):
		data, addr = sock.recvfrom(1024)
		msg = str(data, "utf8")
		print(msg)
		if msg == 'pcaccess':
			try:
				sock.close()
			except Exception as ex:
				print(str(ex))
			return addr
		sleep(3)

def sensor_loop():
	sensor = mpu6050(0x68)
	print("Iniciando...")
	print("Aguardando Conexão..")
	addr = (wait_connect()[0], 24242)
	while(True):
		data = sensor.get_gyro_data()
		Gz = data['z'] / 100 
		Gy = data['y'] / 100
		msg = str(Gy) + "," + str(Gz) + "|"
		udp_send(msg, addr)
		sleep(0.003)


if __name__  == "__main__":
	sensor_loop()
