# JAKA Zu 12 Communication
* JAKA Zu's SSID: CAB12210392
* JAKA Zu's host ip: 10.5.5.100
  * You can use the ethernet port in the box or connect to the wifi to get an IP address assigned(10.5.5.*).
* JAKA Zu's socket server port: 10000
    * It will automatically open when running and send runtime data
    * Data Structure: Json like structure
## Preparation
Connect your computer with Ethernet Cable to the RJ45 socket inside the controller.
~The RJ45 socket at the bottom of the controller will not automatically assign IP address for your computer~
## Usage
**To record a trajectory in joint space:**
`sudo python3 record_teach_traj.py # sudo for socket authorization`
It will automatically create a Traj*.txt in ./traj/ folder.
It will show:
`press enter to proceed`
`press 'q' to quit`
If you press enter, it will print current joint position and record it.
If you press 'q', it will tell you where the trajectory is saved.
**To record a trajectory in TCP center posture:**
`sudo python3 record_ee_pose.py`
Same as above...
**To follow a recorded joint space trajectory**
`sudo python3 follow_traj.py`
It will show `waiting for connection...`
Run the program on JAKA pendant.
`press 'b'+enter to proceed'
