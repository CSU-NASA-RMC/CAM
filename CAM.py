# Main program for CAM, should run on boot
import time
import logging
import remote
import self_test
import manual
import autorun
import threading

logging.basicConfig(filename='CAM.log',
                    format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO) # Log each run

port = 42069  # Carefully chosen

#Do what Houston says
def cam(option):
    global proc
    proc = ""
    logging.info("Executing command: " + option)
    if option == 'HI': # Hello
        return 'HI' # Be polite
    elif option == 'ST': # Self test
        return self_test.self_test()
    elif option == 'MM': # Manual mode
        proc = threading.Thread(target=manual.init, args='', daemon=True)
        return 'OK'
    elif option == 'AR': # Autonomous run
        proc = threading.Thread(target=autorun.init, args='', daemon=True)
        return 'OK'
    elif option == 'SD': # Shutdown
        logging.info("Shutting down")
        logging.shutdown()
        # TODO: Delayed linux shutdown command
        return 'OK'
    elif option == 'SL': # Send logs to Houston
        # TODO: Send logs
        return 'OK'
    else: # Not found
        logging.error("Command not found")
        return 'OK'

if __name__ == "__main__":
    while True:
        remote.listen(cam, port)
        if proc != '':
            logging.info("Starting control thread")
            proc.start()
            proc.join()