'''
Created on 21.11.2014

@author: Group 19
'''

import argparse
from socket import socket, AF_INET, SOCK_STREAM, IPPROTO_TCP


class HttpServer(object):

    '''
    This class represents a simple HTTP server which acts as if it would serve
    one web page and two images
    '''

    def __init__(self, server_ip, server_port):
        '''
        Constructor for storing the IPv4-address of the server and the port
        number
        '''
        # Store the IPv4-address and the port number
        self.server_ip = server_ip
        self.server_port = server_port

    def socket_init(self):
        '''
        Initializes the socket for using an IPv4-address and TCP
        '''
        # IPv4-address: AF_INET
        # TCP: SOCK_STREAM and IPPROTO_TCP
        self.socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)

    def socket_bind(self):
        '''
        Binds the socket to the defined IPv4-address and the port-number
        '''
        self.socket.bind((self.server_ip, self.server_port))
        # Accept only one connection at a time
        self.socket.listen(1)

    def disconnect_client(self):
        '''
        Disconnects the client from the server
        '''
        # Closing the connection
        self.connection.close()
        print "Client disconnected by server", self.client_ip

        # Setting the connection and the IP to None so they can be used for the
        # next connection
        self.connection = None
        self.client_ip = None

    def send_data(self, size):
        '''
        Sends the passed number of bytes (size) of data back to the connected
        client
        '''
        # Create a byte-array with the given size (in byte)
        data = bytearray(size)
        print "Sending back", str(len(data)), "byte of data to the client"
        # Send the data to the client
        self.connection.send(data)

    def start(self):
        '''
        Starts the server. The server listens for incoming connections and processes them.
        The server is configured in a way that it only accepts one connection at a time.
        '''
        # While-True-loop for accepting connections (only one at a time)
        while True:
            # Waiting for client to connect to the server. Create connection
            # after client connects and store clients IPv4-address.
            self.connection, self.client_ip = self.socket.accept()
            print "Client connected: ", self.client_ip

            # As long as the client is not disconnected: serve content
            while True:
                # Waiting for GET-requests from the client
                self.input_buffer = self.connection.recv(1024)

                # Split the lines of the GET-request into arrays (one item for
                # every line)
                self.request = self.input_buffer.splitlines()

                # Check whether the request has to lines according to the task
                if len(self.request) != 2:
                    # If an empty request is received, then the client does not
                    # ask for more content. The client can be disconnected If
                    # more or less then the two lines of a GET-request is
                    # received, disconnect the client as it violated the
                    # specification
                    if self.input_buffer == "":
                        print "No more data is received from the client"
                    else:
                        print "Client sent more or less then 2 lines of the GET-request!"
                    self.disconnect_client()
                    break

                # Check whether the client wants the root web page delivered
                if self.request[0] == "GET / HTTP/1.1" and self.request[1] == "Host:  fakeserver.org":
                    print "Client requested empty-URL path"
                    self.send_data(1024)
                # Check whether the client wants the first picture delivered
                elif self.request[0] == "GET /funny_cat.png HTTP/1.1" and self.request[1] == "Host:  fakeserver.org":
                    print "Client requested funny_cat.png"
                    self.send_data(4096)
                # Check whether the client wants the second picture delivered
                elif self.request[0] == "GET /sad_cat.png HTTP/1.1" and self.request[1] == "Host:  fakeserver.org":
                    print "Client requested sad_cat.png"
                    self.send_data(8192)
                # If none of the requests apply, then the client violated the
                # specification and will be disconnected
                else:
                    print "Client violated the specification!"
                    self.disconnect_client()
                    break

        # This part should not be reached as the server always accepts new
        # connections after the previous one is closed
        print "Server terminated"


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
        help="IPv4-address at which the HTTP-server is reachable. DEFAULT: localhost",
        type=str,
        default="localhost")
    # Add argument for setting the server_port. Set 10080 (http normally uses
    # server_port 80) as default in case no server_port number is passed to
    # the script
    parser.add_argument(
        "--server_port",
        help="Port of the HTTP-server. DEFAULT: 10080",
        type=int,
        default=10080)
    # Finally parse the passed arguments
    args = parser.parse_args()

    # Create http_server
    server = HttpServer(args.server_ip, args.server_port)
    # Initialize the socket (TCP/IP)
    server.socket_init()
    # Bind the socket to the defined IP-address and server port-number
    server.socket_bind()
    
    # Start the server - Accepting connections now
    print "Starting up HTTP server with IP", server.server_ip, \
        "on port", server.server_port
    server.start()

if __name__ == '__main__':
    main()
