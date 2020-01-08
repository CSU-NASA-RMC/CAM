# Interfaces with DWM modules (tags) over a serial connection
# See DWM docs for UART specs
import logging
import serial
import multiprocessing
import time
import statistics

# Handles serial connection to DWM module
class dwm:
    def __init__(self, port):
        logging.info("Initializing DWM module on port: {}".format(port))
        print("Initializing DWM module on port: {}".format(port))
        self.status = "Initializing"

        # Initialize serial connection
        self.ser = serial.Serial()
        self.ser.baudrate = 115200  # Per DWM specs
        self.ser.port = port
        self.ser.timeout = 1
        try:
            # Enter DWM shell mode, start ranging stream
            self.ser.open()

            if self.ser.readline() == b"": # DWM not initialized
                # TODO: If DWM is already initialized w/ no anchors connected output is the same as uninitialized
                # TODO: Improbable case but would cause an issue trying to initialize again
                self.ser.write(b'\r\r')
                time.sleep(1)
                self.ser.write(b'les\r')

                for i in range(20): # Toss out login message
                    self.ser.readline()

            self.status = "Ready"

        except:
            logging.error("Unable to initialize DWM on port: {}".format(port))
            self.status = "Fail"

    # Read les command's output stream
    def read(self):
        if self.status != "Ready":
            return ""

        data = self.ser.readline()
        data = data.decode("utf-8")

        if data.startswith("["): # If anchor is powered on after rover, fw info is printed upon connection
            data = ""

        return data

    # Get ranges from output stream
    def read_range(self):
        # Raw data is of the form "DAB7[2.00,0.00,0.00]=1.25 50B9[0.00,0.00,0.00]=1.63 ..."
        data = self.read()

        if data == "":
            logging.error("Couldn't get any anchor distances")
            return ["ERROR", 0]

        data = data.split(' ')
        ranges = []
        for anchor in data[:-1]: # Last element is return char
            anchor = anchor.split('=')
            dist = anchor[1] # Meters
            name = anchor[0] # Unique for each module, burned into hardware
            name = name.split('[')
            ranges.append([name[0], dist])
        return ranges


# Interfaces with multiple DWM modules to obtain location
class locator:
    def __init__(self, dwm0_port="/dev/ttyUSB1", dwm1_port="/dev/ttyUSB2", buffer_size=5):
        dwm0 = dwm(dwm0_port)
        dwm1 = dwm(dwm1_port)

        # Buffers to hold most recent values
        self.dwm0_buffer = multiprocessing.Queue(5)
        self.dwm1_buffer =  multiprocessing.Queue(5)

        # Iterator threads to handle serial connections (breaks GIL so use Queue to pass data)
        dwm0_iterator = multiprocessing.Process(target=self.dist_buffer, args=(self.dwm0_buffer, dwm0,),
                                                daemon=True)
        dwm1_iterator = multiprocessing.Process(target=self.dist_buffer, args=(self.dwm1_buffer, dwm1,),
                                                daemon=True)
        dwm0_iterator.start()
        dwm1_iterator.start()

    # Fetch values and push to Queue
    def dist_buffer(self, buffer, prov_dwm):
        while True:
            if prov_dwm.status == "Ready":
                if buffer.full():
                    buffer.get()
                buffer.put(prov_dwm.read_range())
            else:
                time.sleep(1) # Otherwise it will pin a thread at 100%

    # Calculate cartesian position given distances of anchors to tag
    def calc_cart(self, d1, d2):
        xc1 = 2 # meters, x coordinate of DWM3 (Positive direction)
        xc2 = 0 # meters, x coordinate of DWM4 (Origin of pit coordinates)

        # This math is wholly derived from the equation for a circle, god speed
        x = d1**2 - d2**2 - xc1**2 + xc2**2
        x *= -1
        x /= 2*xc1 - 2*xc2
        y = d1**2
        y -= (x - xc1)**2
        y = y**0.5
        return [x, y]

    # Calculate position using averaged distances (Assumes 2 anchors)
    def get_pos(self, buffer):
        dists = []
        try:
            while len(dists) < 5: # How many distance readings to average
                dists.append(buffer.get(block=True, timeout=0.5)) # Throws error if queue empty
        except:
            logging.error("Likely lost connection to anchor, aborting position calculation")
            return [-99, -99] # Should look for this value to indicate positioning failure

        dist1 = []
        dist2 = []

        for reading in dists:
            for anchor in reading:
                if anchor[0] == 'DAB7': # Anchor on left of collection bin
                    dist1.append(float(anchor[1]))
                elif anchor[0] == '50B9': # Anchor on right of collection bin
                    dist2.append(float(anchor[1]))

        dist1 = statistics.mean(dist1)
        dist2 = statistics.mean(dist2)

        return self.calc_cart(dist1, dist2)

# Testing
def live_graph(prov_loc): # Live graph of LIDAR data (CPU heavy)
    import matplotlib.pyplot as plt
    import matplotlib.animation as anim

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.xlim(0, 5)
    plt.ylim(0, 5)

    def animate(i):
        data0 = prov_loc.get_pos(test.dwm0_buffer)
        #data1 = prov_loc.get_pos(test.dwm1_buffer)

        print(data0)
        #print(data1)

        #ax.clear()
        ax.scatter(data0[0], data0[1], c='RED')
        #ax.scatter(data1[0], data1[1], c='BLUE')

    ani = anim.FuncAnimation(fig, animate, interval=500)
    plt.show()

if __name__ == "__main__":
    test = locator()
    live_graph(test)
    #while True:
    #    print(test.dwm0_buffer.get())
    #    time.sleep(2)