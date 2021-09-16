from socket import *
import logging
from time import ctime
import time
import os
from pathlib import Path
from utils import *
import argparse

## Parameters
host = ''
port = 1000
ADDR = (host, port)
BUFSIZ = 1024

def follow_traj(args):
    ## Logging
    LOG_NAME = 'Runtime'
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

    ## Load Traj file
    traj_file_path = Path('traj/'+args.path+'.txt')
    traj_file = open(traj_file_path,'r')
    traj = traj_file.readlines()
    traj = convert_traj_file(traj)


    while True:
        ## Handshake
        logging.info('waiting for connection...')
        print('waiting for connection...')
        clientSocket, clientAddr = tcpSocket.accept()
        clientSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        logging.info('conneted form: %s' %clientAddr[0])

        for i in range(len(traj)):
            
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
                    new_pos = traj[i]
                    logging.info('New pos is suppose to be: {}'.format(new_pos))
                    print('New pos is suppose to be: {}'.format(new_pos))
                    print("Moving...")
                    clientSocket.send(str(new_pos).encode('utf-8'))
                    clientSocket.recv(BUFSIZ)
                    pos = clientSocket.recv(BUFSIZ)
                    new_pos = convert_float(pos.decode())
                    print('Movement done! Current pos is: {}'.format(new_pos))
                    logging.info('Current pos is: {}'.format(new_pos))
                    print('{} points to go...'.format(len(traj)-i-1))
                    logging.info(('{} points to go...'.format(len(traj)-i-1)))
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

def convert_traj_file(traj_str):
    traj = []
    for i in range(len(traj_str)):
        traj_current = traj_str[i][:-1].split(', ')
        for j in range(len(traj_current)):
            traj_current[j]=float(traj_current[j])
        traj.append(traj_current)
    return traj
        

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Follow a given trajectory in .txt')
    parser.add_argument('--path', metavar='-p', type=str, help='Import a trajectory here.',default='Traj')
    args = parser.parse_args()
    print(args.path)
    follow_traj(args)