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
        try:
            # Enter DWM shell mode, start ranging stream
            self.ser.open()
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
        else:
            try:
                data = self.ser.readline()
            except:
                data = ""
                self.status = "Fail"
        return data.decode("utf-8")

    # Get ranges from output stream
    def read_range(self):
        # Raw data is of the form "DAB7[2.00,0.00,0.00]=1.25 50B9[0.00,0.00,0.00]=1.63 ..."
        data = self.read()
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