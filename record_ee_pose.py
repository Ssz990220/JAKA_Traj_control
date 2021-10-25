from socket import *
import json
import os
from pathlib import Path
from datetime import datetime
## Parameter
serverName = '10.5.5.100'
serverPort = 10000
BUFSIZ = 4096  # Larger than 3500
ADDR = (serverName,serverPort)
DT = datetime.now()
DT_format = DT.strftime('%Y%m%d%H%M%S')
Traj_name = 'Traj'+DT_format+'_ee'
# Traj_name = 'Traj'

## Traj Dir
Path(os.getcwd()+'/traj').mkdir(exist_ok=True,parents=True)
traj_path = Path('traj/'+Traj_name+'.txt')
traj_path.touch(exist_ok=True)
traj_file = open(traj_path,'a')

## Start Recording
counter = 0
while True:
    counter = counter + 1
    print('Please move to the {} point...\n press \'q\' to quit\n press enter to proceed\n'.format(counter))
    func = input()
    collected = False
    if func == 'q':
        print('Trajector is saved at ',end='')
        print(os.path.join(Path(os.getcwd()+'/traj'),Traj_name))
        break
    else:
        while not collected:
            try:
                clientSocket = socket(AF_INET, SOCK_STREAM)
                clientSocket.connect(ADDR)
                returnData = clientSocket.recv(BUFSIZ)
                Data = json.loads(returnData.decode())
                print(Data['actual_position'])
                traj_file.write(str(Data['actual_position'])[1:-1]+'\n')
                clientSocket.close()
                collected = True
            except json.decoder.JSONDecodeError:
                continue
    