from time import sleep
import RPi.GPIO as gpio


DIR = 6
STEP = 13

DIR2 = 16
STEP2 = 12

LED = 25
LEDON = 1
LEDOFF = 0

CW =1
CCW =0

gpio.setmode(gpio.BCM)

gpio.setup(DIR, gpio.OUT)
gpio.setup(STEP, gpio.OUT)
gpio.output(DIR,CW)

gpio.setup(DIR2, gpio.OUT)
gpio.setup(STEP2, gpio.OUT)
gpio.output(DIR2,CW)

gpio.setup(LED, gpio.OUT)
gpio.output(LED,LEDON)

try:
    while True:
        sleep(1)
        gpio.output(DIR,CW)
        gpio.output(DIR2,CW)
        for x in range(3200):
            gpio.output(STEP,gpio.HIGH)
            gpio.output(STEP2,gpio.HIGH)
            sleep(.0010)
            gpio.output(STEP,gpio.LOW)
            gpio.output(STEP2,gpio.LOW)
            sleep(.0010)
        
        sleep(1)
        gpio.output(DIR,CCW)
        gpio.output(DIR2,CCW)
        for x in range(3200):
            gpio.output(STEP,gpio.HIGH)
            gpio.output(STEP2,gpio.HIGH)
            sleep(.0001)
            gpio.output(STEP,gpio.LOW)
            gpio.output(STEP2,gpio.LOW)
            sleep(.0001)
            
except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    gpio.cleanup()