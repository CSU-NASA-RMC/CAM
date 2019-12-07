# Basic format of an autonomous runfile
import time

file_version = 0.2 # Retain compatibility

# This will be called by Houston
def control(status, motors, lidar):
    # Code here will run once
    motors.stop(False) # Hard stop motors
    i = 0
    while True:
        # Code here will run on a loop

        # Get sensor data, do stuff, etc.
        i += 1
        time.sleep(1)

        # Post a status to be retrieved by Houston
        status.put("Value has reached: {}".format(i))

        # Perform some check for completion
        if i == 10:
            motors.stop(True) # Smooth stop motors
            return # Exit control script
