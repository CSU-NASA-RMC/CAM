# Manual control of robot from houston
import logging
import remote
import motor

port = 42070 # For network


def handler(input):
    global motors

    if input == 'STOP':
        motors.stop()
        return 'CC'

    input = input.split(',')

    in_type = input[0]
    in_diff = input[1]
    input = input[2:]  # Trim out mode

    # Handle axis input
    # 0 'ABS_X'       Left stick horizontal   -1=left
    # 1 'ABS_Y'       Left stick vertical     -1=up
    # 2 'ABS_RX'      Right stick horizontal  -1=left
    # 3 'ABS_RY'      Right stick vertical    -1=up
    # 4 'ABS_Z'       Left trigger            0=unpressed
    # 5 'ABS_RZ'      Right trigger           0=unpressed
    # 6 'ABS_HAT0X'   D-Pad horizontal        -1=left
    # 7 'ABS_HAT0Y'   D-Pad vertical          -1=up
    if in_type == 'axis':
        if in_diff == 'Easy':
            print("easy mode, axis")

        elif in_diff == 'Advanced':
            print("advanced mode, axis")

    # Handle button input
    # BTN_SOUTH     A
    # BTN_EAST      B
    # BTN_NORTH     X
    # BTN_WEST      Y
    # BTN_TL        Left bumper
    # BTN_TR        Right bumper
    # BTN_SELECT    Select, unsurprisingly
    # BTN_START     Start
    # BTN_MODE      Xbox button
    # BTN_THUMBR    Right stick click
    # BTN_THUMBL    Left stick click
    elif in_type == 'btn':
        if in_diff == 'Easy':
            print("easy mode, button")

        elif in_diff == 'Advanced':
            print("advanced mode, button")

    # TODO do something with inputs

    return "OK"


def init(prov_mot):
    logging.info("Beginning manual control mode")

    # Send motor handler to global scope for network handlers to access
    global motors
    motors = prov_mot

    remote.listen(handler, port, True) # Listen to Houston


# Testing
if __name__ == "__main__":
    init(motor.motors)