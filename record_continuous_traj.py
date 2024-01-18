from socket import *
import json
import os
import time
from pathlib import Path
from datetime import datetime
import threading


stop_flag = False

def input_function():
    global stop_flag
    input("Press Enter to stop")
    stop_flag = True

def main_loop():
    ## Parameter
    serverName = '192.168.125.3'
    serverPort = 10000
    BUFSIZ = 4096  # Larger than 3500
    ADDR = (serverName, serverPort)
    DT = datetime.now()
    DT_format = DT.strftime('%Y%m%d%H%M%S')
    Traj_name = 'Traj' + DT_format
    # Traj_name = 'Traj'

    ## Traj Dir
    Path(os.getcwd() + '/traj').mkdir(exist_ok=True, parents=True)
    traj_path = Path('traj/' + Traj_name + '.txt')
    traj_path.touch(exist_ok=True)
    traj_file = open(traj_path, 'a')

    ## Start Recording
    counter = 0
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(ADDR)

    dataReceived = ''

    global stop_flag

    while not stop_flag:
        # print('Please move to the {} point...\n press \'q\' to quit\n press enter to proceed\n'.format(counter))
        # func = input()
        # time.sleep(0.005)
        # # # collected = False
        # if func == 'q':
        #     print('Trajector is saved at ', end='')
        #     print(os.path.join(Path(os.getcwd() + '/traj'), Traj_name))
        #     break
        # else:
        #     while not collected:
        try:
            returnData = clientSocket.recv(BUFSIZ)
            Data = json.loads(returnData.decode())
            # traj_file = open(traj_path, 'a')
            # print(Data['joint_actual_position'])
            # traj_file.write(str(Data['joint_actual_position'])[1:-1] + ' '+ str(time.time()) + '\n')
            dataReceived += str(Data['joint_actual_position'])[1:-1] + ' ' + str(time.time()) + '\n'
            # traj_file.close()
            # print(frame_rates)
            # collected = True
        except json.decoder.JSONDecodeError:
            continue
        except KeyboardInterrupt:
            traj_file.close()

    traj_file.write(dataReceived)


loop_thread = threading.Thread(target = main_loop)
loop_thread.start()

input_thread = threading.Thread(target = input_function)
input_thread.start()

input_thread.join()

loop_thread.join()

print("STOPPED")
