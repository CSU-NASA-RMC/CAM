# Handle the motor controllers

def stop():
    print("All motors stop")

def wheel(num, speed):
    print("Wheel #/Speed", num, speed)

def tank(left, right):
    wheel(0, left)
    wheel(1, right)
    wheel(2, left)
    wheel(3, right)