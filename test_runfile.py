# Basic format of an autonomous runfile
import multiprocessing
import time
import motor

file_version = 0.0 # Retain compatibility

# This will be called by Houston
def control(status):
    # Code here will run once
    motor.stop()
    i = 0
    while True:
        # Code here will run on a loop

        # Get sensor data, do stuff, etc.
        i += 1
        time.sleep(1)

        # Post a status to be retrieved by Houston
        status.put("Value has reached: {}".format(i))

        # Perform some check for completion
        if i == 20:
            return # Exit control script