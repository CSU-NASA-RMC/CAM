# CAM
This is the main rover program. A service is intended to run on boot of the main control computer to manage all systems. These programs were designed for a Linux x86_64 environment, specifically Debain 10 on a LattePanda Alpha 864s. It's recommended that you use Pycharm Pro as your IDE.

## How to use the rover
* Plug the router into a power source
* Connect your computer to the router
* Connect the rover's battery
* Hold power button on side of control box for 3 seconds
* Launch the [Houston utility](https://github.com/CSU-NASA-RMC/houston)

*For manual control, the Xbox controller must be connected to your computer before launching Houston*

## Update rover from Github repo
* Connect to the rover via SSH
* Change into the CAM directory (/home/cam/CAM)
* Run the following commands

        systemctl --user stop cam.service
        git pull
        sudo reboot

## Update rover from local repo
* Set up [Remote Debug Configuration](https://www.jetbrains.com/help/pycharm/remote-debugging-with-product.html#remote-debug-config) for a Pycharm Pro project in a local CAM directory
* Connect to rover via SSH and run

        systemctl stop cam.service
* Tools>Deployment>Upload to *xxx*
* Connect to rover via SSH and run

        systemctl start cam.service

## Connect as Remote Debugger
* Set up [Remote Debug Configuration](https://www.jetbrains.com/help/pycharm/remote-debugging-with-product.html#remote-debug-config) for a Pycharm Pro project in a local CAM directory
* Set your computer's IP in CAM.py for pydevd
* Connect to rover via SSH
* Start debug server on your computer
* Run the following command

        systemctl --user restart cam.service
* You are now connected to the interpreter running on the rover
