# Provide interface with RPLidar S1 using lidar.o
# lidar.o is the compilation output "ultra_simple" from RPLidar SDK
# Compiled to run on linux x86_64
# Available here: https://www.slamtec.com/en/Support#rplidar-s1

import logging
import subprocess
import threading
import collections
import time

# Process LIDAR data and send to buffer
def read_output(process, append, fov):
    for line in iter(process.stdout.readline, ""):
        try:
            meas = line.decode('utf-8').split(' ')
            angle = float(meas[4])
            dist = float(meas[6])
            quality = float(meas[8])

            if angle >= fov[0] and angle <= fov[1]:  # Within FOV
                append([angle, dist, quality])

        except:
            logging.debug("Bad lidar data", meas)

# Create object to connect to LIDAR
class lidar:
    def __init__(self, buffer_size = 1000, field_of_view = [0, 360]):
        logging.info("Starting lidar")

        # This all obeys GIL so there *shouldn't* be race conditions
        self.buffer = collections.deque(maxlen=buffer_size) # Buffer to hold most recent values
        self.proc = subprocess.Popen("./lidar.o", stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Iterator thread to keep buffer updated

        self.info = [] # Diagnostic info
        for i in range(6): # First 6 lines contain diagnostics
            self.info.append(self.proc.stdout.readline().decode('utf-8').split(':'))

        # Toss out first readings as sensor spools up
        for i in range(1000):
            self.proc.stdout.readline()

        # Start iterator
        self.t = threading.Thread(target=read_output, args=(self.proc, self.buffer.append, field_of_view))
        self.t.daemon = True
        self.t.start()


# Testing
if __name__ == "__main__":
    test = lidar(buffer_size=2000, field_of_view=[0, 180])
    print("Initialized")
    time.sleep(1)
    print("Printing buffer")
    print(test.buffer[0][0])
    time.sleep(2)
    print(test.buffer[0])
    time.sleep(2)
    print(test.buffer[0])