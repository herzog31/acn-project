"""
ACN Project
SSH Server

@author: Group 19
"""

import argparse
import socket

class SSHServer:
    """
    This class implements a static ssh server

    Usage:
        * Init with server ip (localhost) and the port the server should
          listen to
        * Create socket with socket_init()
        * Bind the socket to the port with socket_bind()
        * Listen for incoming connections using start()
    """

    def __init__(self, server_ip, server_port):
        """
        Create an instance of the SSH server
        """
        self.server_ip = server_ip
        self.server_port = server_port
        self.command_count = 0

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

    def close_connection(self):
        """
        Close the connection of the current client. Server is then able to
        listen to a new client.
        """
        print "Disconnect: Client", self.client_addr
        self.connection.close()
        self.connection = None
        self.client_addr = None
        self.command_count = 0

    def ack_command(self, command):
        """
        Send an acknowledge message for the given command to the client
        """
        self.connection.sendall("ACKNOWLEDGE " + command)
        print "Server (" + str(self.command_count + 1) + "): ACKNOWLEDGE " +\
             command
        self.command_count += 1

    def start(self):
        """
        Server is listening to connection requests. Once a connection is
        established, the server sends a welcome message and waits for the
        client to send commands.
        """
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

            self.close_connection()


def main():
    """
    Argparse to specify the server's ip & port in the console
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ip",
        help="""IP address at which the ssh server is reachable.
        DEFAULT: localhost""",
        type=str,
        default="localhost")
    parser.add_argument(
        "--port",
        help="Port of the ssh server. DEFAULT: 10022",
        type=int,
        default=10022)
    args = parser.parse_args()

    # Initialize SSH server and execute protocol
    server = SSHServer(args.ip, args.port)
    server.socket_init()
    server.socket_bind()
    server.start()

if __name__ == '__main__':
    main()