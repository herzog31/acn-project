"""
ACN Project
FTP Client

@author: Group 19
"""

import argparse
import socket
import timeit

class FTPClient:
    """
    This class implements a static ftp client

    Usage:
        * Init with server ip & port
        * Init socket with socket_init()
        * Connect to server with socket_connect(). The client then waits for 
          the FTP server's welcome message.
    """

    def __init__(self, server_ip, server_port, debug):
        """
        Create client with server ip & port
        """
        self.server_ip = server_ip
        self.server_port = server_port
        self.debug = debug

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
        if self.debug:
            print "Disconnect: Server", (self.server_ip, self.server_port)

    def request_file(self):
        """
        Send a FTP request to the server to request the file bigdata.tar.xz
        """
        if self.debug:
            print "Client: " + "get bigdata.tar.xz"
        self.socket.sendall("get bigdata.tar.xz")
        self.listen_for_file()

    def listen_for_file(self):
        """
        Wait for the server to respond to the request_file() method and 
        receive any data the server sends
        """
        file = ""
        while True:
            buffer = self.socket.recv(1024)
            file += str(buffer)
            if not buffer:
                break
        if self.debug:
            print "Server: File of length " + str(len(file))

    def listen_for_welcome(self):
        """
        Listen for the FTP server's welcome message
        """
        while True:
            buffer = self.socket.recv(1024)
            if buffer[:3] == "220":
                if self.debug:
                    print "Server: " + buffer
                self.request_file()
            break
        self.socket_disconnect()


def main():

    """
    Argparse to specify the server's ip & port in the console
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ip",
        help="IP address of the ftp server. DEFAULT: localhost",
        type=str,
        default="localhost")
    parser.add_argument(
        "--port",
        help="Port of the ftp server. DEFAULT: 10021",
        type=int,
        default=10021)
    parser.add_argument(
        "--debug",
        help="Print out additional debug information",
        action="store_true")
    parser.set_defaults(debug=False)
    args = parser.parse_args()

    # Start execution time measurement 
    start_time = timeit.default_timer()

    # Initialize FTP client and execute protocol
    client = FTPClient(args.ip, args.port, args.debug)
    client.socket_init()
    client.socket_connect()

    # End execution time measurement and print results
    end_time = timeit.default_timer()
    execution_time = (end_time - start_time) * 1000  # in ms

    if args.debug:
        print "Execution time was " + str(execution_time) + " ms"
    else:
        print str(execution_time)

if __name__ == '__main__':
    main()