# Begin autonomous run
import remote
import importlib
import logging
import multiprocessing

port = 42071 # Port for communication

script = None # Runfile to execute

# Get runfile from houston
def get_name(name):
    global script
    try:
        logging.info("Loading file: " + name)
        script = importlib.import_module(name) # Import runfile as module
        return 'OK'
    except:
        logging.error("Load failed") # Probably filename was not found
        return 'LOAD FAIL'

# Set up and start a run
def init():
    global script
    logging.info("Beginning autonomous run")
    remote.listen(get_name, port) # Get name from Houston
    if script is None: # Error loading, logged in get_name
        return

    # Program will run as separate process
    logging.info("Launching script")
    status = multiprocessing.Queue()
    loop = multiprocessing.Process(target=script.control, args=(status,))
    loop.daemon = True

    # Do as houston says
    def listen(cmd):
        # Kill process
        if cmd == "KP":
            logging.info("Killing autonomous script")
            loop.terminate()
            return "CC"

        # Start process
        elif cmd == "GO":
            if loop.exitcode == None and not loop.is_alive():
                logging.info("Starting autonomous script")
                loop.start()
                return "OK"
            else:
                logging.error("Instructed to start already running script")
                return "NO"

        # Get status of process
        elif cmd == "0":
            logging.info("Sending status of autonomous script")
            if loop.exitcode == None: # Not yet finished
                if loop.is_alive(): # Still running
                    msg = "LIVE" # Falls through if no status provided
                    while not status.empty(): # Get message from top of stack
                        msg = status.get()
                    return msg
                else: # Not started
                    return "READY"
            else: # Exited
                return "FINISHED"

    remote.listen(listen, port, True) # Listens on a loop
    logging.info("Autonomous run complete")