import argparse
import socket
import timeit

class SSHClient:

	def __init__(self, server_ip, server_port, commands):
		self.server_ip = server_ip
		self.server_port = server_port
		self.command_count = 0
		self.commands = commands
		print(self.commands)

	def socket_init(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

	def socket_connect(self):
		self.socket.connect((self.server_ip, self.server_port))
		self.listen_for_welcome()

	def socket_disconnect(self):
		self.socket.close()
		print "Disconnect: Server", (self.server_ip, self.server_port)

	def listen_for_welcome(self):
		while True:
			buffer = self.socket.recv(1024)
			print "Server: "+buffer
			break

	# def send_commands(self):


	# def send_command(self, index):

	# def listen_for_ack(self, index):



def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("ip", help="IP address of the ssh server", type=str)
	parser.add_argument("--port", help="Port of the ssh server, e.g. 10022", type=int, default=10022)
	args = parser.parse_args()

	start_time = timeit.default_timer()

	commands = ["testA", "testB", "testC", "testD", "testE"]
	
	client = SSHClient(args.ip, args.port, commands)
	client.socket_init()
	client.socket_connect() 
	

	end_time = timeit.default_timer()
	execution_time = (end_time - start_time) * 1000 # in ms

	print "Execution time was " + str(execution_time) + " ms"

if __name__ == '__main__':
    main()