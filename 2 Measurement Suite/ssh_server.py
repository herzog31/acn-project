import argparse
import socket

class SSHServer:

	def __init__(self, server_ip, server_port):
		self.server_ip = server_ip
		self.server_port = server_port
		self.command_count = 0

	def socket_init(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

	def socket_bind(self):
		self.socket.bind((self.server_ip, self.server_port))
		self.socket.listen(1)

	def close_connection(self):
		print "Disconnect: Client", self.client_addr
		self.connection.close()
		self.connection = None
		self.client_addr = None
		self.command_count = 0

	def ack_command(self, command):
		self.connection.sendall("ACK " + command)
		print "Server (" + str(self.command_count + 1) + "): ACK " + command
		self.command_count += 1

	def start(self):
		while True:
			self.connection, self.client_addr = self.socket.accept()
			print "Connect: Client", self.client_addr
			print "Server: " + "SSH-0.0-Insecure"
			self.connection.sendall("SSH-0.0-Insecure")
			
			while True:
				buffer = self.connection.recv(1024)

				if not buffer:
					break

				if buffer == "logout":
					print "Client: " + buffer
					break

				print "Client: " + buffer
				self.ack_command(buffer)
			
			self.close_connection();

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--ip", help="IP address at which the ssh server is reachable. DEFAULT: localhost", type=str, default="localhost")
	parser.add_argument("--port", help="Port of the ssh server. DEFAULT: 10022", type=int, default=10022)
	args = parser.parse_args()

	server = SSHServer(args.ip, args.port)
	server.socket_init()
	server.socket_bind()
	server.start()

if __name__ == '__main__':
    main()