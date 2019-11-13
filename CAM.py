# Main program for CAM, should run on boot
import time
import remote
import self_test
import manual
import auto

port = 42069  # Carefully chosen

#Do what Houston says
def cam(option):
    print(option)
    if option == b'HI': # Hello
        return b'HI' # Be polite
    elif option == b'ST': # Self test
        return self_test.self_test()
    elif option == b'MM': # Manual mode
        return b'OK'
        manual.init()
    elif option == b'AR': # Autonomous run
        return b'OK'
        auto.init()
    elif option == b'SD': # Shutdown
        print("Shutting down")
        return b'OK'
        # TODO: Linux shutdown command

if __name__ == "__main__":
    while True:
        remote.listen(cam, port)