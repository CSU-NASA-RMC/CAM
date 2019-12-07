# Begin autonomous run
import remote
import importlib
import logging
import multiprocessing
import motor
import lidar

port = 42071 # Port for communication

script = None # Runfile to execute

started = None # If thread has been run

# Get runfile from houston
def get_name(name):
    global script
    global started
    try:
        logging.info("Loading file: " + name)
        script = importlib.import_module(name) # Import runfile as module
        started = False
        return 'OK'
    except:
        logging.error("Load failed") # Probably filename was not found
        return 'LOAD FAIL'

# Set up and start a run
def init(prov_mot, prov_lidar):
    global script
    logging.info("Beginning autonomous run")
    remote.listen(get_name, port) # Get name from Houston
    if script is None: # Error loading, logged in get_name
        return

    # Program will run as separate process
    logging.info("Launching script")
    status = multiprocessing.Queue()
    loop = multiprocessing.Process(target=script.control, args=(status, prov_mot, prov_lidar,))
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
            global started
            if not started:
                logging.info("Starting autonomous script")
                loop.start()
                started = True
                return "OK"
            else:
                logging.error("Script can only be run once")
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

if __name__ == "__main__":
    init(motor.motors(), lidar.lidar())