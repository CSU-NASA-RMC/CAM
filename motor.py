# Handle the motor controllers
import logging

# TODO lots
# Should spawn a separate thread with a queue to pass in commands
# Should be time dependent to implement PID control
# This object is going to be thrown around between processes, do what they say safely
# Will need to integrate with motor controllers using serial to Arduino or pyFirmata
# Should have a watchdog timer in case of connection loss/parent crash

class motors:
    def __init__(self):
        self.stop()

        self.status = "OK" # TODO: real status checks

    def stop(self, smooth=False):
        logging.info("Stopping motors")
        print("All motors stop") # Filler
        return "OK"

    def wheel(self, num, speed):
        print("Wheel #/Speed", num, speed) # Filler

    def tank(self, left, right):
        self.wheel(0, left)
        self.wheel(1, right)
        self.wheel(2, left)
        self.wheel(3, right)

# Testing
if __name__ == "__main__":
    test = motors
    test.stop(False)