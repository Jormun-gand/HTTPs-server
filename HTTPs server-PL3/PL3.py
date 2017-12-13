
import ssl

from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", 8080))  
serverSocket.listen(1)
while True:
    # Establish the connection
    print('Ready to serve...')
    newSocket, addr = serverSocket.accept()
    connectionSocket = ssl.wrap_socket(newSocket, server_side=True, certfile='server.pem', keyfile='server.pem', ciphers='ALL')
    try:
        message = (connectionSocket.recv(1024)).decode('utf-8')
        if message is None or message.__eq__(""):
            continue
        message = message.strip()
        print("[",message,"]")
        filename = message.split()[1]
        f = open(filename[1:], "rb")
        outputdata = f.read()
        f.close()
        connectionSocket.send(b'HTTP/1.1 200 OK\r\nContent-type:text/html;charset=utf8\r\n\r\n')
        connectionSocket.send(outputdata)
        connectionSocket.send(b'\r\n')
        connectionSocket.shutdown(SHUT_RDWR)
        connectionSocket.close()
    except IOError:
        # Your code
        connectionSocket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
        connectionSocket.send(b"<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n")
        connectionSocket.shutdown(SHUT_RDWR)
        connectionSocket.close()

serverSocket.close()
