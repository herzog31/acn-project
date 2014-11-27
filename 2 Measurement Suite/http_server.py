'''
Created on 21.11.2014

@author: Group 19
'''

import argparse
from socket import socket, AF_INET, SOCK_STREAM, IPPROTO_TCP

class http_server(object):
    '''
    This class represents a simple HTTP server which acts as if it would serve one web page and two images.
    '''


    def __init__(self, ip, port):
        '''
        Constructor for storing the IPv4-address of the server and the port number
        '''
        self.server_ip = ip
        self.server_port = port
        
        
    def socket_init(self):
        '''
        Initializes the socket for using an IPv4-address and TCP
        '''
        # IPv4-address: AF_INET
        # TCP: SOCK_STREAM and IPPROTO_TCP
        self.socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
        
    def socket_bind(self):
        '''
        Binds the socket to the defined IPv4-address and the server_port-number
        '''
        self.socket.bind((self.server_ip, self.server_port))
        # Accept only one connection at a time
        self.socket.listen(1)
        
    def normalize_line_endings(self, request):
        '''Convert string containing various line endings like \n, \r or \r\n,
        to uniform \n.'''
    
        return ''.join((line + '\n') for line in request.splitlines())   
    
    def disconnect_client(self):
        '''
        This method disconnects the client from the server
        '''
        print "Client disconnected by server", self.client_ip
        self.connection.close()
        self.connection = None
        self.client_ip = None
        
    def send_data(self, size):
        '''
        Sends the passed number of bytes (size) of data (zeros) back to the connected client.
        '''
        data = bytearray(size)
        print "Sending back data to the client:", str(len(data)), "Byte"
        self.connection.send(data)
        
    def start(self):
        '''
        Starts the server. The server listens for incoming connections and processes them.
        The server is configured in a way that it only accepts one connection at a time.
        '''
        while True:
            self.connection, self.client_ip = self.socket.accept()
            print "Client connected: ", self.client_ip
            
            while True:
                self.input_buffer = self.connection.recv(1024)
                
                if self.input_buffer:
                    print "echo input_buffer ->",self.input_buffer
                
                self.request = self.input_buffer.splitlines()
                if len(self.request) != 2:
                    if self.input_buffer == "":
                        print "No more data is received from the client"
                    else:
                        print "Client sent more or less then 2 lines of the GET-request!"
                    self.disconnect_client()
                    break
                    
                if self.request[0] == "GET / HTTP/1.1" and self.request[1] == "Host:  fakeserver.org":
                    print "Client requested empty-URL path"
                    self.send_data(1024)
                elif self.request[0] == "GET /funny_cat.png HTTP/1.1" and self.request[1] == "Host:  fakeserver.org":
                    print "Client requested funny_cat.png"
                    self.send_data(4096)
                elif self.request[0] == "GET /sad_cat.png HTTP/1.1" and self.request[1] == "Host:  fakeserver.org":
                    print "Client requested sad_cat.png"
                    self.send_data(8192)
                else:
                    print "Client violated the specification!"
                    self.disconnect_client()
                    break
        

def main():
    '''
    This is the main function that first parses the passed arguments (IP-address and server_port)
    and then creates and starts the HTTP server.
    '''
    
    # Initialize argument parser
    parser = argparse.ArgumentParser()
    # Add argument for setting the IPv4-address. Set localhost as default in case no IP-address is passed to the script
    parser.add_argument("--server_ip", help="IPv4-address at which the HTTP-server is reachable. DEFAULT: localhost", type=str, default="localhost")
    # Add argument for setting the server_port. Set 10080 (http normally uses server_port 80) as default in case no server_port number is passed to the script
    parser.add_argument("--server_port", help="Port of the HTTP-server. DEFAULT: 10080", type=int, default=8080)
    # Finally parse the passed arguments
    args = parser.parse_args()

    # Create http_server
    server = http_server(args.server_ip, args.server_port)
    # Initialize the socket (TCP/IP)
    server.socket_init()
    # Bind the socket to the defined IP-address and server_port-number
    server.socket_bind()
    # Start the server - Accepting connections now
    print "Starting up server with IP", server.server_ip,"on port", server.server_port
    server.start()

if __name__ == '__main__':
    # Initializing the main function that is called when the script is run
    main()
