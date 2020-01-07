# Interfaces with DWM modules (tags) over a serial connection
# See DWM docs for UART specs
import logging
import serial
import io
import collections
import time

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
            return []

        data = data.split(' ')
        ranges = []
        for anchor in data[:-1]: # Last element is return char
            anchor = anchor.split('=')
            dist = anchor[1]
            name = anchor[0]
            name = name.split('[')
            ranges.append([name[0], dist])
        return ranges


if __name__ == "__main__":
    test = dwm("/dev/ttyUSB0")
    while True:
        print(test.read_range())