# Begin autonomous run
import remote
import importlib
import logging

port = 42070

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

def init():
    logging.info("Beginning autonomous run")
    remote.listen(get_name, port)
    if script == None:
        exit(1)
    script.loop()