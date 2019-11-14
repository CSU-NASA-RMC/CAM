# Handle the motor controllers
import logging

def stop():
    print("All motors stop") # Filler

def wheel(num, speed):
    print("Wheel #/Speed", num, speed) # Filler

def tank(left, right):
    wheel(0, left)
    wheel(1, right)
    wheel(2, left)
    wheel(3, right)