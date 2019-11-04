# Main program for CAM, should run on boot
import time
import remote
import self_test

if __name__ == "__main__":
    # Tell houston we are booting up, wait for response
    while True:
        try:
            if remote.send(b"RUNNING CHECKS") == b"OK": break
        except:
            print("Connect fail, retrying in 5 sec")
            time.sleep(5)

    # Run self checks and get operating mode
    mode = remote.send(self_test.self_test())

    print("Operating mode: ", mode)