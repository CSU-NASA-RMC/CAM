# CAM
This is the main rover program. A service is intended to run on boot of the main control computer to manage all systems. These programs were designed for a Linux x86_64 environment namely Debain 10 on a LattePanda Alpha 864s. To send commands, use the [houston utility](https://github.com/CSU-NASA-RMC/houston) from a computer on the same network.

## Update rover
* Connect to the rover via SSH
* Change into the CAM directory (/home/cam/CAM)
* Run the following commands

        systemctl --user stop cam.service
        git pull
        systemctl --user start cam.service
