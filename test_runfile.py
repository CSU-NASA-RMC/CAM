# Basic format of an autonomous runfile
import time
import motor

file_version = 0.0 # Retain compatibility

# This will be called by Houston
def control():
    # Code here will run once
    motor.stop()
    i = 0
    while True:
        # Code here will run on a loop

        # Get sensor data, do stuff, etc.
        # Dummy code
        i += 1
        time.sleep(1)

        # Check for completion
        if i == 10:
            return # Exit control script