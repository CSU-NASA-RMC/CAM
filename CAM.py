# Main program for CAM, should run on boot
import logging
import remote
import self_test
import manual
import autorun
import multiprocessing

logging.basicConfig(filename='CAM.log',
                    format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.DEBUG) # Log each run to file

port = 42069  # Port for communication

proc = None # Control thread

# Do what Houston says
def cam(option):
    global proc
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
        return 'OK' # It's done

    # Self test
    elif option == 'ST':
        return self_test.self_test()

    # Manual mode
    elif option == 'MM':
        # Spawn as separate process
        proc = multiprocessing.Process(target=manual.init, args='')
        proc.start()
        return 'OK'

    # Autonomous run
    elif option == 'AR':
        # Spawn as separate process
        proc = multiprocessing.Process(target=autorun.init, args='')
        proc.start()
        return 'OK'

    # Shutdown
    elif option == 'SD':
        logging.info("Shutting down")
        logging.shutdown()
        # TODO: Delayed linux shutdown command
        return 'CC'

    # Send logs to Houston
    elif option == 'SL':
        # TODO
        return 'OK'

    # Retrieve runfile from houston
    elif option == 'UP':
        # TODO
        return 'OK'

    # Not found
    else:
        logging.error("Command not found")
        return 'NO'

# Runs on boot of CAM
if __name__ == "__main__":
    logging.info("Starting up")
    remote.listen(cam, port, True) # Listens on a loop