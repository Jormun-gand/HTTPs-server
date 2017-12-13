#-*- coding: utf-8 -*-
#import socket module
#Assignment 1: Web Server
#In this assignment, you will develop a simple Web server in Python
#that is capable of retrieving static HTML files and processing one request at a time.
#Specifically, your Web server will
#(i) create a connection socket when contacted by a client (browser);
#(ii) receive the HTTP request from this connection;
#(iii) parse the request to determine the specific file being requested;
#(iv) get the requested file from the server’s file system;
#(v) create an HTTP response message consisting of the requested file preceded
#by header lines;
#(vi) send the response over the TCP connection to the requesting browser.
#If a browser requests a file that is not presentin your server,
#your server should return a “404 Not Found” error message.

from socket import*
serverSocket = socket(AF_INET, SOCK_STREAM)
"""
Prepare a sever socket
"""

serverSocket.bind(('', 8080))# binds address to socket， ''indicate all available interfaces
serverSocket.listen(1)
#conn, addr = serverSocket.accept()


while True:
    #Establish the connection
    print 'Ready to serve...'
    connectionSocket, addr = serverSocket.accept()
    #print 'connected from',addr
    try:
        message = connectionSocket.recv(1024)
        filename = message.split()[1]
        print filename
        f = open(filename[1:])
        outputdata = f.read()
        """
        Send one HTTP header line into socket
        """
        #Your code
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n")

        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i])
        connectionSocket.send("\r\n")

        # Close the client connection socket
        connectionSocket.close()

    except IOError:
        """
        Send response message for file not found
        """
        #Your code
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n")
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n")
        """
        Close client socket
        """
        connectionSocket.close()

serverSocket.close()
