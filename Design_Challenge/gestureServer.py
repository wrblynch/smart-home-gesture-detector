from socket import *

#Prepare a server socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 9879
serverAddress = '127.0.0.1'

serverSocket.bind((serverAddress, serverPort))
serverSocket.listen(3)

while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        #Recover message from client
        message = connectionSocket.recv(1024)
        message = message.decode()
        print("Received message: " + message)
    except IOError:
        connectionSocket.close()

serverSocket.close()
sys.exit()