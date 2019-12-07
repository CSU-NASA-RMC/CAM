# Test systems
import logging
import lidar
import motor
import time

def self_test(prov_motor, prov_lidar):
    logging.info("Starting self test")


    # Test LIDAR sensor
    if prov_lidar.info == "FAIL":
        return "LIDAR FAIL"
    if len(prov_lidar.info[5]) != 2:
        return "LIDAR FAIL"
    elif prov_lidar.info[5][1] != ' 0\n':
        return "LIDAR FAIL"
    elif prov_motor.status != "OK":
        return "MOTOR FAIL"

    # TODO: Perform rest of tests
    return "PASS" #Pretend all is OK


# Testing
if __name__ == "__main__":
    mot = motor.motors()
    lid = lidar.lidar()
    time.sleep(1)
    print(self_test(mot, lid))