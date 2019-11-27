# Test systems
import logging
import lidar

def self_test():
    logging.info("Starting self test")

    # Test LIDAR sensor
    test_lidar = lidar.lidar()
    if test_lidar.info[5][1] != ' 0\n':
        return "LIDAR FAIL"

    # TODO: Perform rest of tests
    return "PASS" #Pretend all is OK


# Testing
if __name__ == "__main__":
    print(self_test())