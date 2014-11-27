"""
ACM Project
FTP Server

@author: Group 19
"""

import argparse
import socket

class FTPServer:
	"""
	This class implements a static ftp server

	Usage:
		* Init with server ip (localhost) and the port the server should
		  listen to
		* Create socket with socket_init()
		* Bind the socket to the port with socket_bind()
		* Listen for incoming connections using start()
	"""

	def __init__(self, server_ip, server_port):
		"""
		Create an instance of the FTP server
		"""
		self.server_ip = server_ip
		self.server_port = server_port

	def socket_init(self):
		"""
		Initialize the socket used for sending and receiving packets
		"""
		self.socket = socket.socket(
			socket.AF_INET,
			socket.SOCK_STREAM,
			socket.IPPROTO_TCP)

	def socket_bind(self):
		"""
		Bind socket to the server's ip and listening port
		"""
		self.socket.bind((self.server_ip, self.server_port))
		self.socket.listen(1)

	def get_file(self):
		"""
		In response to a client's get file request send a file consisting of 
		zeros
		"""
		size = 128 * 1024
		file = "".join("%01x" % b for b in bytearray(size))
		print "Server: File of length " + str(len(file)) + " Bytes"
		self.connection.sendall(file)

	def close_connection(self):
		"""
		Close the connection of the current client. Server is then able to 
		listen to a new client.
		"""
		print "Disconnect: Client", self.client_addr
		self.connection.close()
		self.connection = None
		self.client_addr = None

	def start(self):
		"""
		Server is listening to connection requests. Once a connection is 
		established, the server sends a welcome message and waits for any get 
		file requests.
		"""
		while True:
			self.connection, self.client_addr = self.socket.accept()
			print "Connect: Client", self.client_addr
			print "Server: " + "220 Welcome to " + self.server_ip
			self.connection.sendall("220 Welcome to " + self.server_ip)
			while True:
				buffer = self.connection.recv(1024)
				if buffer[:3] == "get":
					print "Client: " + buffer
					self.get_file()
					self.close_connection()
					break
				break


def main():
	"""
	Argparse to specify the server's ip & port in the console
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"--ip",
		help="""IP address at which the ftp server is reachable. 
		DEFAULT: localhost""",
		type=str,
		default="localhost")
	parser.add_argument(
		"--port",
		help="Port of the ftp server. DEFAULT: 10021",
		type=int,
		default=10021)
	args = parser.parse_args()

	# Initialize FTP server and execute protocol
	server = FTPServer(args.ip, args.port)
	server.socket_init()
	server.socket_bind()
	server.start()

if __name__ == '__main__':
	main()