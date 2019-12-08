# Handle the motor controllers
import logging


class motors:
    def heartbeat(self):
        # Provide beat for watchdog to enable drivers
        while self.status == "OK":
            #TODO
            pass

    # TODO PID Control for each motor
    # TODO Limit checks
    # TODO Integrate with pyfirmata

    # Wheel FL
    def FL(self, speed):
        return

    # Wheel FR
    def FR(self, speed):
        return

    # Wheel RL
    def RL(self, speed):
        return

    # Wheel RR
    def RR(self, speed):
        return

    # Auger
    def aug(self, speed):
        return

    # Slider
    def sld(self, speed):
        return

    # Tilt-mining
    def tlt(self, speed):
        return

    # Deposit bucket
    def bkt(self, speed):
        return

    def __init__(self):
        self.status = "Initializing"
        self.stop()

        self.status = "OK" # TODO: real status check (arduinos present, etc)

    def stop(self, smooth=False):
        logging.info("Stopping motors")
        self.FL(0)
        self.FR(0)
        self.RL(0)
        self.RR(0)
        self.aug(0)
        self.sld(0)
        self.tlt(0)
        self.bkt(0)
        return self.status

    # Map wheel number to motors
    def wheel(self, num, speed):
        if num == 0:
            self.FL(speed)
        elif num == 1:
            self.FR(speed)
        elif num == 2:
            self.RL(speed)
        elif num == 3:
            self.RR(speed)

    # Map L,R tank drive to wheel number
    def tank(self, left, right):
        self.wheel(0, left)
        self.wheel(1, right)
        self.wheel(2, left)
        self.wheel(3, right)

    # Map X,Y from joystick to L,R tank drive
    def direction(self, speed, dir):
        # Math from http://home.kendra.com/mauser/joystick.html
        v = (1-abs(dir))*speed+speed
        w = (1-abs(speed))*dir+dir
        l = (v+w)/2
        r = (v-w)/2

        self.tank(l, r)


# Testing
if __name__ == "__main__":
    test = motors()
    test.stop(False)