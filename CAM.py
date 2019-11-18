# Main program for CAM, should run on boot
import time
import logging
import remote
import self_test
import manual
import autorun
import multiprocessing

logging.basicConfig(filename='CAM.log',
                    format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.DEBUG) # Log each run

port = 42069  # Carefully chosen

proc = None # Control thread

# Do what Houston says
def cam(option):
    global proc
    logging.info("Executing command: " + option)
    if option == 'HI': # Get status
        if proc is None:
            return 'HI' # Ready for command
        elif proc.is_alive():
            logging.warning("Possible broken connection")
            return 'BZ' # Busy
        else:
            return 'HI'
    elif option == 'KP': # Kill process
        logging.warning("Killing process")
        proc.terminate()
        return 'OK' # It's done
    elif option == 'ST': # Self test
        return self_test.self_test()
    elif option == 'MM': # Manual mode
        proc = multiprocessing.Process(target=manual.init, args='')
        proc.start()
        return 'OK'
    elif option == 'AR': # Autonomous run
        proc = multiprocessing.Process(target=autorun.init, args='')
        proc.start()
        return 'OK'
    elif option == 'SD': # Shutdown
        logging.info("Shutting down")
        logging.shutdown()
        # TODO: Delayed linux shutdown command
        return 'CC'
    elif option == 'SL': # Send logs to Houston
        # TODO: Send logs
        return 'OK'
    else: # Not found
        logging.error("Command not found")
        return 'OK'

# Runs on boot of CAM
if __name__ == "__main__":
    logging.info("Starting up")
    remote.listen(cam, port, True)