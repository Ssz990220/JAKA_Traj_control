from socket import *
import json

serverName = '10.5.5.100'
serverPort = 10000
BUFSIZ = 4096
ADDR = (serverName,serverPort)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(ADDR)
returnData = clientSocket.recv(BUFSIZ)
Data = json.loads(returnData.decode())
print(Data['joint_actual_position'])
clientSocket.close()