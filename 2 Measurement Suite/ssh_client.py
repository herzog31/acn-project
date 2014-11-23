import argparse
import socket
import timeit

class SSHClient:

	def __init__(self, server_ip, server_port, commands):
		self.server_ip = server_ip
		self.server_port = server_port
		self.command_index = 0
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

	def logout(self):
		self.socket.sendall("logout")
		print "Client: logout"

	def listen_for_welcome(self):
		buffer = self.socket.recv(1024)
		print "Server: "+buffer
		self.send_commands()

	def send_commands(self):
		while self.command_index < len(self.commands):
			self.send_command()
			if self.listen_for_ack():
				self.command_index += 1
			else:
				break
		self.logout()
		self.socket_disconnect()

	def send_command(self):
		print "Client (" + str(self.command_index + 1) + "): " + self.commands[self.command_index % len(self.commands)]
		self.socket.sendall(self.commands[self.command_index % len(self.commands)])

	def listen_for_ack(self):
		while True:
			buffer = self.socket.recv(1024)
			if buffer == "ACK " + self.commands[self.command_index % len(self.commands)]:
				print "Server: "+buffer
				return True
			return False



def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("ip", help="IP address of the ssh server", type=str)
	parser.add_argument("--port", help="Port of the ssh server, e.g. 10022", type=int, default=10022)
	args = parser.parse_args()

	start_time = timeit.default_timer()

	commands = ["testA", "testB", "testC", "testD", "testE", "testF", "testG", "testH", "testI", "testJ"]
	
	client = SSHClient(args.ip, args.port, commands)
	client.socket_init()
	client.socket_connect() 
	
	end_time = timeit.default_timer()
	execution_time = (end_time - start_time) * 1000 # in ms

	print "Execution time was " + str(execution_time) + " ms"

if __name__ == '__main__':
    main()