from socket import *
from time import ctime
import datetime
import logging
import time
import os
from pathlib import Path

host = ''
port = 1000
ADDR = (host, port)
BUFSIZ = 1024
e = datetime.datetime.now()
LOG_NAME = (e.strftime('%m%d%H%M%S'))
# LOG_NAME = 'runtime'

## Logging
logfile = Path('log/'+LOG_NAME+'.log')
logfile.touch(exist_ok=True)
print(os.path.dirname(__file__))
print('Logging at ',logfile)
logging.basicConfig(filename=logfile, filemode='w+', 
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    datefmt="%d-%m-%Y %H:%M:%S", level=logging.DEBUG)

## Setup TCP Server
tcpSocket = socket(AF_INET, SOCK_STREAM)
tcpSocket.bind(ADDR)
tcpSocket.listen(5) #set the max number of tcp connection

while True:
    ## Handshake
    logging.info('waiting for connection...')
    clientSocket, clientAddr = tcpSocket.accept()
    logging.info('conneted form: %s' %clientAddr[0])


    while True:
        
        try:
            var_flag = clientSocket.recv(BUFSIZ).decode()[5:-1]
            var_val = input('Waiting for your command:')
            message = '<'+var_flag+'><\"'+var_val+'\">'
            clientSocket.send(message.encode('utf-8'))
            logging.info('Message sent: '+message)
            data = clientSocket.recv(BUFSIZ)
            if data.decode() == 'no':
                continue
            pos = clientSocket.recv(BUFSIZ)
        except IOError as e:
            logging.ERROR(e)
            clientSocket.close()
            break
        if not data:
            break
        returnData = 'Data received is :' + data.decode('utf-8') + pos.decode('utf-8')
        print(returnData)
        # clientSocket.send(returnData.encode('utf-8'))
    clientSocket.close()
tcpSocket.close()