# Main program for CAM, should run on boot
import logging
import remote
import self_test
import manual
import autorun
import multiprocessing
import motor
import lidar
import os

logging.basicConfig(filename='CAM.log',
                    format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO) # Log each run to file

port = 42069  # Port for communication

proc = None # Control thread

motors = motor.motors() # Motor manager
main_lidar = lidar.lidar() # LIDAR manager

# Do what Houston says
def cam(option):
    global proc
    global motors
    global main_lidar

    logging.info("Executing command: " + option)

    # Get status
    if option == 'HI':
        # No running process
        if proc is None:
            return 'HI' # Ready for command

        # Abandoned process
        elif proc.is_alive():
            logging.warning("Possible broken connection")
            return 'BZ' # Busy

        # Previous process finished
        else:
            return 'HI'

    # Kill process
    elif option == 'KP':
        logging.warning("Killing process")
        proc.terminate()
        motors.stop(False)  # Hard stop motors
        return 'OK' # It's done

    # Self test
    elif option == 'ST':
        return self_test.self_test(motors, main_lidar)

    # Manual mode
    elif option == 'MM':
        # Spawn as separate process
        proc = multiprocessing.Process(target=manual.init, args=(motors, main_lidar,))
        proc.start()
        return 'OK'

    # Autonomous run
    elif option == 'AR':
        # Spawn as separate process
        proc = multiprocessing.Process(target=autorun.init, args=(motors, main_lidar,))
        proc.start()
        return 'OK'

    # Shutdown
    elif option == 'SD':
        logging.info("Shutting down")
        logging.shutdown()
        os.system('(sleep 5 ; sudo poweroff) &')
        return 'CC'

    # Not found
    else:
        logging.error("Command not found")
        return 'NO'


# Runs on boot of CAM
if __name__ == "__main__":
    print("Begin listening")
    logging.info("Starting up")
    remote.listen(cam, port, True) # Listens on a loop
    while True:
        pass # Hold for shutdown command to go through
