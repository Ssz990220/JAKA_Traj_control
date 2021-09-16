from socket import *
import logging
from time import ctime
import time
import os
from pathlib import Path
from utils import *

host = ''
port = 1000
ADDR = (host, port)
BUFSIZ = 1024
# e = datetime.datetime.now()
# LOG_NAME = (e.strftime('%m%d%H%M%S'))
LOG_NAME = 'Runtime'

## Logging
logfile = Path('log/'+LOG_NAME+'.log')
logfile.touch(exist_ok=True)
print(os.path.dirname(__file__))
print('Logging at',logfile)
logging.basicConfig(filename=logfile, filemode='a', format="%(asctime)s %(levelname)s:%(message)s", datefmt="%d-%m-%Y %H:%M:%S", level=logging.INFO)

## Setup TCP Server
tcpSocket = socket(AF_INET, SOCK_STREAM)
tcpSocket.bind(ADDR)
tcpSocket.listen(5) #set the max number of tcp connection
tcpSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
while True:
    ## Handshake
    logging.info('waiting for connection...')
    print('waiting for connection...')
    clientSocket, clientAddr = tcpSocket.accept()
    clientSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    logging.info('conneted form: %s' %clientAddr[0])

    while True:
        
        try:
            var_flag = clientSocket.recv(BUFSIZ).decode()[5:-1]
            var_val = input('Waiting for your command: ')
            if var_val == 'q':
                clientSocket.close()
                tcpSocket.close()
                break
            logging.info('Input is '+str(var_val))
            message = '<'+var_flag+'><\"'+var_val+'\">'
            clientSocket.send(message.encode('utf-8'))
            logging.info('Message sent: '+message)
            data = clientSocket.recv(BUFSIZ)
            if not data:
                break
            elif data.decode() == '0':
                logging.info('No')
                print('No')
                continue
            else:
                pos = clientSocket.recv(BUFSIZ)
                new_pos = convert_float(pos.decode())
                print(new_pos)
                for i in range(6):
                    new_pos[i] = new_pos[i] + 1
                clientSocket.send(str(new_pos).encode('utf-8'))
                print(clientSocket.recv(BUFSIZ))
                pos = clientSocket.recv(BUFSIZ)
                new_pos = convert_float(pos.decode())
                print(new_pos)
                
        except:
            clientSocket.close()
            tcpSocket.close()
            raise IOError
        returnData = 'Data received is :' + data.decode('utf-8') + pos.decode('utf-8')
        logging.info(returnData)
        # clientSocket.send(returnData.encode('utf-8'))
    if var_val == 'q':
        break
tcpSocket.close()


