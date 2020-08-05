from time import sleep
import RPi.GPIO as gpio


DIR = 16
STEP = 12

CW =1
CCW =0

gpio.setmode(gpio.BCM)
gpio.setup(DIR, gpio.OUT)
gpio.setup(STEP, gpio.OUT)
gpio.output(DIR,CW)

# Main body of code
try:
    while True:
        sleep(1)
        gpio.output(DIR,CW)
        for x in range(3200):
            gpio.output(STEP,gpio.HIGH)
            sleep(.0010)
            gpio.output(STEP,gpio.LOW)
            sleep(.0010)
        
        sleep(1)
        gpio.output(DIR,CCW)
        for x in range(3200):
            gpio.output(STEP,gpio.HIGH)
            sleep(.0001)
            gpio.output(STEP,gpio.LOW)
            sleep(.0001)
            
except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    gpio.cleanup()