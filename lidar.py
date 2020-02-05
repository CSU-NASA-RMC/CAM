# Provide interface with RPLidar S1 using lidar.o
# lidar.o is the compilation output "ultra_simple" from RPLidar SDK
# Compiled to run on linux x86_64
# Available here: https://www.slamtec.com/en/Support#rplidar-s1

import logging
import subprocess
import threading
import collections
from bisect import bisect_left

# Create object to connect to LIDAR
class lidar:
    # Get distance from closest reference point
    def get_deviation(self, measurement):
        pos = bisect_left(self.ref_angles, measurement[0]) # Get position of closest angle, O(log n) sort time
        return self.reference[pos][1] - measurement[1]

    # Process LIDAR data and send to buffer
    def read_output(self, process, append, fov):
        try:
            for line in iter(process.stdout.readline, ""):
                try:
                    meas = line.decode('utf-8').split(' ')
                    angle = float(meas[4])
                    dist = float(meas[6])
                    quality = float(meas[8])
                    dev = self.get_deviation([angle, dist])

                    if fov[0] <= angle <= fov[1] and dist > 0:  # Within FOV and real reading
                        append([angle, dist, dev, quality])

                except:
                    logging.debug("Bad lidar data")
        except:
            logging.error("No lidar data")
            append([0, 0, 0])  # Dummy data

    def load_ref(self):
        # Load reference terrain (flat ground)
        ref_file = open("lidar_ref.csv", "r+")  # Reference terrain file
        self.reference = []
        for line in ref_file.readlines():
            line = line.split(',')
            angle = float(line[0])
            line = line[1].split('\n')
            dist = float(line[0])
            self.reference.append([angle, dist])
        ref_file.close()
        self.ref_angles = [item[0] for item in self.reference]

    def __init__(self, buffer_size = 1200, field_of_view = [90, 270], testing=False):
        logging.info("Starting lidar")
        self.info = "Starting"

        try:
            # This all obeys GIL so there *shouldn't* be race conditions
            self.buffer = collections.deque(maxlen=buffer_size) # Buffer to hold most recent values

            if testing: # If running in IDE
                path = "./lidar.o" # Pycharm runs in the project folder
            else:
                path = "/home/cam/CAM/lidar.o" # System service requires absolute path or path from CAM home folder

            self.proc = subprocess.Popen(path, stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)  # Start lidar.o with piped output

            self.info = [] # Diagnostic info
            for i in range(6): # First 6 lines contain diagnostics
                self.info.append(self.proc.stdout.readline().decode('utf-8').split(':'))

            # Toss out first readings as sensor spools up
            for i in range(1000):
                self.proc.stdout.readline()

            self.load_ref()

            # Start iterator
            self.t = threading.Thread(target=self.read_output, args=(self.proc, self.buffer.append, field_of_view))
            self.t.daemon = True
            self.t.start()

            while len(self.buffer) < buffer_size: # Block until buffer is populated
                pass

            self.info = "READY"
        except:
            logging.error("LIDAR could not be started")

            # Junk data so other stuff doesn't crash
            self.info = "FAIL"
            self.buffer = [[0, 0, 0]]

    # Read data for reference terrain and save
    def calibrate(self):
        if self.info != "READY": # Only calibrate if LIDAR is working
            return "NO"

        ref_file = open("lidar_ref.csv", "w+") # Empties file and opens for write
        data = list(self.buffer)
        data.sort() # Reference list must be sorted for use of bisect_left for search

        for point in data:
            ref_file.write("{},{}\n".format(point[0], point[1])) # CSV format
        ref_file.close()

        self.load_ref()


# Testing
def live_graph(prov_lid): # Live graph of LIDAR data (CPU heavy)
    import matplotlib.pyplot as plt
    import matplotlib.animation as anim

    fig = plt.figure()
    ax = fig.add_subplot(1, 2, 1, projection='polar')
    ax2 = fig.add_subplot(1, 2, 2)

    def animate(i):
        data = prov_lid.buffer
        angles = []
        dists = []
        devs = []
        quals = []
        for point in data:
            angles.append((360 - point[0]) / 180 * 3.1415)
            dists.append(point[1])
            devs.append(point[2])
            quals.append(point[3])
        ax.clear()
        ax2.clear()
        ax.scatter(angles, dists, s=10, c=quals)
        ax2.scatter(angles, devs, s=10)

    ani = anim.FuncAnimation(fig, animate, interval=100)
    plt.show()


if __name__ == "__main__":
    import time
    test = lidar(buffer_size=600, field_of_view=[90, 270], testing=True)
    test.calibrate()
    live_graph(test)
