"""
ACM Project
SSH Client

@author: Group 19
"""

import argparse
import socket
import timeit

class SSHClient:
    """
    This class implements a static ssh client

    Usage:
            * Init client with server ip, port and array with commands that 
              should be sent to the server
            * Init socket with socket_init()
            * Connect to server with socket_connect(). The client then waits 
              for the SSH server's welcome message
    """

    def __init__(self, server_ip, server_port, commands):
        """
        Create client with server ip, port and array with commands
        """
        self.server_ip = server_ip
        self.server_port = server_port
        self.command_index = 0
        self.commands = commands
        print(self.commands)

    def socket_init(self):
        """
        Initialize the socket used for sending and receiving packets
        """
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_TCP)

    def socket_connect(self):
        """
        Connect to the previously specified server
        """
        self.socket.connect((self.server_ip, self.server_port))
        self.listen_for_welcome()

    def socket_disconnect(self):
        """
        Disconnect from the server
        """
        self.socket.close()
        print "Disconnect: Server", (self.server_ip, self.server_port)

    def logout(self):
        """
        Send the logout command to the SSH server
        """
        self.socket.sendall("logout")
        print "Client: logout"

    def listen_for_welcome(self):
        """
        Listen for the SSH server's welcome message
        """
        buffer = self.socket.recv(1024)
        print "Server: " + buffer
        self.send_commands()

    def send_commands(self):
        """
        Iterate through the command array and send each command to the server 
        and wait for an acknowledgement for each command from the server
        """
        while self.command_index < len(self.commands):
            self.send_command()
            if self.listen_for_ack():
                self.command_index += 1
            else:
                break
        self.logout()
        self.socket_disconnect()

    def send_command(self):
        """
        Send individual command at the index self.command_index to the server
        """
        print "Client (" + str(self.command_index + 1) + "): " +\
            self.commands[self.command_index % len(self.commands)]
        self.socket.sendall(
            self.commands[
                self.command_index % len(
                    self.commands)])

    def listen_for_ack(self):
        """
        Listen for the SSH server's acknowledgement for the previously sent 
        command at index self.command_index
        """
        while True:
            buffer = self.socket.recv(1024)
            if buffer == "ACKNOWLEDGE " + \
                    self.commands[self.command_index % len(self.commands)]:
                print "Server: " + buffer
                return True
            return False


def main():
    """
    Argparse to specify the server's ip & port in the console
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ip",
        help="IP address of the ssh server. DEFAULT: localhost",
        type=str,
        default="localhost")
    parser.add_argument(
        "--port",
        help="Port of the ssh server. DEFAULT: 10022",
        type=int,
        default=10022)
    args = parser.parse_args()

    # Start execution time measurement
    start_time = timeit.default_timer()

    # Array with commands the client should sent to the server
    commands = [
        "testA",
        "testB",
        "testC",
        "testD",
        "testE",
        "testF",
        "testG",
        "testH",
        "testI",
        "testJ"]

    # Initialize SSH client and execute protocol
    client = SSHClient(args.ip, args.port, commands)
    client.socket_init()
    client.socket_connect()

    # End execution time measurement and print results
    end_time = timeit.default_timer()
    execution_time = (end_time - start_time) * 1000  # in ms

    print "Execution time was " + str(execution_time) + " ms"

if __name__ == '__main__':
    main()