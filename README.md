# CAM
This is the main rover program. The script cam.sh is intended to run on boot of the main control computer to manage all systems. These programs were designed for a Linux x86_64 environment namely Debain 10 on a LattePanda Alpha 864s. To send commands, use the [houston utility](https://github.com/CSU-NASA-RMC/houston) from a computer on the same network.

## Update rover
* Connect to the rover via SSH
* Exit the login script by pressing Ctrl+C
* Change into the CAM directory (/home/cam/CAM as of writing)
* Run the following commands to pull changes from the master tree and reload CAM.py

        killall python3
        git pull
        sudo reboot
