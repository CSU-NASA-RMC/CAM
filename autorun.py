# Begin autonomous run
import remote
import importlib
import logging
import multiprocessing
import time

port = 42071

script = None # Will get from Houston

# Get name, import, and acknowledge
def get_name(name):
    global script
    try:
        logging.info("Loading file: " + name)
        script = importlib.import_module(name)
        return 'OK'
    except:
        logging.error("Load failed")
        return 'LOAD FAIL'

# Set up and start a run
def init():
    global script
    logging.info("Beginning autonomous run")

    # Get name from Houston
    remote.listen(get_name, port)

    # Program loops
    logging.info("Launching script")
    loop = multiprocessing.Process(target=script.control, args='')
    loop.start()
    logging.info("Waiting for script to exit")
    loop.join()  # TODO: Crash detection
    logging.info("Autonomous run complete")