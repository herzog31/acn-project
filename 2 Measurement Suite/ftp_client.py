import argparse
import socket
import timeit

class FTPClient:

	def __init__(self, server_ip, server_port):
		self.server_ip = server_ip
		self.server_port = server_port

	def socket_init(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

	def socket_connect(self):
		self.socket.connect((self.server_ip, self.server_port))
		self.listen_for_welcome()

	def socket_disconnect(self):
		self.socket.close()
		print "Disconnect: Server", (self.server_ip, self.server_port)

	def request_file(self):
		print "Client: " + "get bigdata.tar.xz"
		self.socket.sendall("get bigdata.tar.xz")
		self.listen_for_file()

	def listen_for_file(self):
		file = ""
		while True:
			buffer = self.socket.recv(1024)
			file += str(buffer)
			if not buffer:
				break
		print "Server: File of length " + str(len(file))

	def listen_for_welcome(self):
		while True:
			buffer = self.socket.recv(1024)
			if buffer[:3] == "220":
				print "Server: "+buffer
				self.request_file()
			break
		self.socket_disconnect()

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--ip", help="IP address of the ftp server. DEFAULT: localhost", type=str, default="localhost")
	parser.add_argument("--port", help="Port of the ftp server. DEFAULT: 10021", type=int, default=10021)
	args = parser.parse_args()

	start_time = timeit.default_timer()

	client = FTPClient(args.ip, args.port)
	client.socket_init()
	client.socket_connect()

	end_time = timeit.default_timer()
	execution_time = (end_time - start_time) * 1000 # in ms

	print "Execution time was " + str(execution_time) + " ms"

if __name__ == '__main__':
    main()


