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
        # Dummy code
        i += 1
        print(i)
        status.put("Value has reached: {}".format(i))
        time.sleep(1)

        # Check for completion
        if i == 20:
            return # Exit control script