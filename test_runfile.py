# Basic format of an autonomous runfile
import motor

file_version = 0.0 # Retain compatibility

# Put code here to loop
def loop():
    # Main control loop

    # Get sensor data

    # Process it

    # Do stuff

    # etc.

    # Update status every loop
    if 1 == 1:
        status = "Ok" # Log any string
    else:
        status = False # Loop will not run again when set to False

# Commands sent from Houston will run this code, passing the input as cmd
def command(cmd):
    # Do stuff with command
    response = "do {} yourself".format(cmd)
    return response