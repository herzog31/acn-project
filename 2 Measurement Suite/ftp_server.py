import argparse
from socket import *

class ftp_server:

	def __init__(self, server_ip, server_port):
		self.server_ip = server_ip
		self.server_port = server_port

	def socket_init(self):
		self.socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)

	def socket_bind(self):
		self.socket.bind((self.server_ip, self.server_port))
		self.socket.listen(1)

	def get_file(self):
		size = 128 * 1024
		file = "".join("%01x" % b for b in bytearray(size))
		print "Server: File of length "+str(len(file))+" Bytes"
		self.connection.sendall(file)

	def close_connection(self):
		print "Disconnect: Client", self.client_addr
		self.connection.close()
		self.connection = None
		self.client_addr = None

	def start(self):
		while True:
			self.connection, self.client_addr = self.socket.accept()
			print "Connect: Client", self.client_addr
			print "Server: "+"220 Welcome to "+self.server_ip
			self.connection.sendall("220 Welcome to "+self.server_ip)
			while True:
				buffer = self.connection.recv(1024)
				if buffer[:3] == "get":
					print "Client: " + buffer
					self.get_file()
					self.close_connection()
					break
				break

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--ip", help="IP address at which the ftp server is reachable, e.g. localhost", type=str, default="localhost")
	parser.add_argument("--port", help="Port of the ftp server, e.g. 10021", type=int, default=10021)
	args = parser.parse_args()

	server = ftp_server(args.ip, args.port)
	server.socket_init()
	server.socket_bind()
	server.start()

if __name__ == '__main__':
    main()