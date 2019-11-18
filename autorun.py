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
    remote.listen(get_name, port) # Get name from Houston

    # Program loops
    logging.info("Launching script")
    status = multiprocessing.Queue()
    loop = multiprocessing.Process(target=script.control, args=(status,))
    loop.daemon = True

    def listen(cmd):
        if cmd == "KP":
            logging.info("Killing autonomous script")
            loop.terminate()
            return "CC"
        elif cmd == "GO":
            logging.info("Starting autonomous script")
            loop.start()
            return "OK"
        elif cmd == "0":
            logging.info("Sending status of autonomous script")
            if loop.exitcode == None:
                if loop.is_alive():
                    return str(status.get())
                else:
                    return "READY"
            else:
                return "FINISHED"

    remote.listen(listen, port, True)
    logging.info("Autonomous run complete")