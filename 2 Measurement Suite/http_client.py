'''
Created on 23.11.2014

@author: Group 19
'''

import argparse
import timeit
from socket import socket, AF_INET, SOCK_STREAM, IPPROTO_TCP

class http_client(object):
    '''
    This class represents a simple HTTP client which tries to get a web page from the HTTP server and two images.
    '''


    def __init__(self, server_ip, server_port):
        '''
        Constructor for storing the IPv4-address of the server and the port number
        '''
        self.server_ip = server_ip
        self.server_port = server_port
        
    def socket_init(self):
        '''
        Initializes the socket for using an IPv4-address and TCP
        '''
        # IPv4-address: AF_INET
        # TCP: SOCK_STREAM and IPPROTO_TCP
        self.socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
        
    def socket_connect(self):
        '''
        Connects to the server with the defined IPv4-address with the given port
        '''
        self.socket.connect((self.server_ip, self.server_port))
        print "Client connected to server", self.server_ip, "on port", self.server_port
        
    def socket_disconnect(self):
        '''
        Disconnects from the server
        '''
        self.socket.close()
        print "Client disconnected from server", self.server_ip
        
    def fetch_web_page(self):
        '''
        Client requests the web page with its two images
        '''
        self.socket.send("GET / HTTP/1.1\nHost:  fakeserver.org")
        self.buffer1 = self.socket.recv(1024)
        print "Root web page received from server"
        
        self.socket.send("GET /funny_cat.png HTTP/1.1\nHost:  fakeserver.org")
        self.buffer2 = self.socket.recv(4096)
        print "funny_cat.png received from server"
        
        self.socket.send("GET /sad_cat.png HTTP/1.1\nHost:  fakeserver.org")
        self.buffer3 = self.socket.recv(8192)
        print "sad_cat.png received from server"
        
def main():
    '''
    This is the main function that first parses the passed arguments (IP-address and server_port)
    and then creates and starts the HTTP server.
    '''
    # Initialize argument parser
    parser = argparse.ArgumentParser()
    # Add argument for setting the IPv4-address. Set localhost as default in case no IP-address is passed to the script
    parser.add_argument("--server_ip", help="IPv4-address of the HTTP-server to which the client should connect.", type=str, default="localhost")
    # Add argument for setting the server_port. Set 10080 (http normally uses server_port 80) as default in case no server_port number is passed to the script
    parser.add_argument("--server_port", help="Port of the HTTP-server to which the client should connect. DEFAULT 10080", type=int, default=8080)
    # Finally parse the passed arguments
    args = parser.parse_args()

    # Create HTTP client (not part of the time measurement
    client = http_client(args.server_ip, args.server_port)
    
    # Start measurement
    start_time = timeit.default_timer()

    client.socket_init()
    client.socket_connect()

    # Fetch the web page
    client.fetch_web_page()

    client.socket_disconnect()
    
    # Finish measurement
    end_time = timeit.default_timer()
    
    # Calculate and show execution time
    execution_time = (end_time - start_time) * 1000  # in ms
    print "Execution time was", str(execution_time), "ms"

if __name__ == '__main__':
    # Initializing the main function that is called when the script is run
    main()
