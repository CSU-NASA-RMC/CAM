# Basic format of an autonomous runfile

file_version = 0.0 # Retain compatibility

# Put code here to loop
def loop():
    print("Wow it worked!")
    # Main control loop

    # Get sensor data

    # Process it

    # Do stuff

    # etc.

    # Update status every loop
    if 1 == 1:
        status = "All good here" # Send any string to Houston
    else:
        status = False # Loop will not run again

# Commands sent from Houston will run this code, passing the input as cmd
def command(cmd):
    # Do stuff with command
    response = "do {} yourself".format(cmd)
    return response