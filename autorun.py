# Begin autonomous run
import remote
import importlib
import logging
import multiprocessing

port = 42070

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

# Pass commands
def pass_commands():
    global script
    while True:
        remote.listen(script.command, port)
        #TODO: Fix this part

# Set up and start a run
def init():
    logging.info("Beginning autonomous run")

    # Get name from Houston
    remote.listen(get_name, port)
    if script == None:
        return

    # Start program loops
    logging.info("Launching script")
    loop = multiprocessing.Process(target=script.control, args='')
    listener = multiprocessing.Process(target=pass_commands, args='')
    loop.start()
    listener.start()
    logging.info("Waiting for script to exit")
    loop.join()  # TODO: Crash detection
    listener.terminate()
    logging.info("Autonomous run complete")