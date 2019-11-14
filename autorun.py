# Begin autonomous run
import remote
import importlib

port = 42070

# Get name, import, and acknowledge
def get_name(name):
    global script
    try:
        print(name)
        script = importlib.import_module(name)
        return 'OK'
    except:
        return 'LOAD FAIL'
        exit(1)

def init():
    print("Beginning autonomous run")
    remote.listen(get_name, port)
    script.loop()