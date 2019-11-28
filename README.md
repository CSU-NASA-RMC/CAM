# CAM
This is the main rover program. It is intended to run on boot of the main control computer to manage all systems. Designed for a Linux x86_64 environment. To send commands, use the houston utility.

## Update rover
* Connect to the rover via SSH
* Exit the login script by pressing Ctrl+C
* Change into the CAM directory (/home/cam/CAM as of writing)
* Run the following commands to pull changes from the master tree and reload CAM.py

        killall *python*
        git pull
        sudo reboot
