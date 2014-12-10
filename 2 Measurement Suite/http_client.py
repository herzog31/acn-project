'''
Created on 23.11.2014
ACN Project
HTTP Client

@author: Group 19
'''

import argparse
import timeit
from socket import socket, AF_INET, SOCK_STREAM, IPPROTO_TCP


class HttpClient(object):

    '''
    This class represents a simple HTTP client which tries to get a web page
    and two images from a simple HTTP server.
    '''

    def __init__(self, server_ip, server_port, debug):
        '''
        Constructor for storing the IPv4-address of the server and the port
        number
        '''
        # Store the IPv4-address and the port number
        self.server_ip = server_ip
        self.server_port = server_port
        self.debug = debug

    def socket_init(self):
        '''
        Initializes the socket for using an IPv4-address and TCP
        '''
        # IPv4-address: AF_INET
        # TCP: SOCK_STREAM and IPPROTO_TCP
        self.socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)

    def socket_connect(self):
        '''
        Connects to the server with the defined
        IPv4-address with the given port
        '''
        # Connect to the server using the IPv4-address and the port number
        self.socket.connect((self.server_ip, self.server_port))

        if self.debug:
            print "Client connected to server", self.server_ip, \
                "on port", self.server_port

    def socket_disconnect(self):
        '''
        Disconnect from the server
        '''
        # Close the connection and hence the socket
        self.socket.close()
        if self.debug:
            print "Client disconnected from server", self.server_ip

    def fetch_web_page(self):
        '''
        Client requests the web page with its two images
        '''

        # GET-request for the root web page
        self.socket.sendall("GET / HTTP/1.1\nHost:  fakeserver.org")
        # Receiving the root web page
        buffer1 = self.socket.recv(1024)
        if self.debug:
            print "Root web page received from server"

        # GET-request for the first image "funny_cat.png"
        self.socket.sendall("GET /funny_cat.png HTTP/1.1\nHost:  fakeserver.org")
        # Receiving the first image
        buffer2 = self.socket.recv(4096)
        if self.debug:
            print "funny_cat.png received from server"

        # GET-request for the second image "sad_cat.png"
        self.socket.sendall("GET /sad_cat.png HTTP/1.1\nHost:  fakeserver.org")
        # Receiving the second image
        buffer3 = self.socket.recv(8192)
        if self.debug:
            print "sad_cat.png received from server"


def main():
    '''
    This is the main function that first parses the passed arguments
    (IP-address and server_port) and then creates and starts the HTTP server.
    '''
    # Initialize argument parser
    parser = argparse.ArgumentParser()
    # Add argument for setting the IPv4-address. Set localhost as default in
    # case no IP-address is passed to the script
    parser.add_argument(
        "--server_ip",
        help="IPv4-address of the HTTP-server to which the client should connect.",
        type=str,
        default="localhost")
    # Add argument for setting the server_port. Set 10080 (http normally uses
    # server_port 80) as default in case no server_port number is passed to
    # the script
    parser.add_argument(
        "--server_port",
        help="Port of the HTTP-server to which the client should connect. DEFAULT 10080",
        type=int,
        default=10080)
    parser.add_argument(
        "--debug",
        help="Print out additional debug information",
        action="store_true")
    parser.set_defaults(debug=False)
    # Finally parse the passed arguments
    # If "-h" or "--help" is passed, then the help message is printed
    args = parser.parse_args()

    # Create HTTP client (not part of the time measurement)
    client = HttpClient(args.server_ip, args.server_port, args.debug)

    # Start measurement
    start_time = timeit.default_timer()

    # Initialize the socket
    client.socket_init()
    # Connect to the server
    client.socket_connect()
    # Fetch the web page
    client.fetch_web_page()
    # Disconnect from the server
    client.socket_disconnect()

    # Finish measurement
    end_time = timeit.default_timer()

    # Calculate and show execution time in ms
    execution_time = (end_time - start_time) * 1000
    if args.debug:
        print "Execution time was", str(execution_time), "ms"
        print "Client terminated"
    else:
        print str(execution_time)

if __name__ == '__main__':
    main()
