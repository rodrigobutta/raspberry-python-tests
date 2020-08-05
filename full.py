import RPi.GPIO as gpio
from datetime import datetime
from time import sleep

# Button codes regarding test IR controller:
# Button Code - up: 0x300ff18e7
# Button Code - down: 0x300ff4ab5
# Button Code - right: 0x300ff5aa5
# Button Code - left: 0x300ff10ef
# Button Code - okk: 0x300ff38c7

PULSE = .00001
STEPS = 1

GPIO_IR = 17
Buttons = [0x300ff18e7, 0x300ff4ab5,
           0x300ff5aa5, 0x300ff10ef, 0x300ff38c7, 0x3]
ButtonsNames = ["UP", "DOWN", "RIGHT", "LEFT", "OK", "PRESSED"]

lastCommand = ""

GPIO_DIR = 6
GPIO_STEP = 13

GPIO_DIR2 = 16
GPIO_STEP2 = 12

GPIO_LED = 25

LEDON = 1
LEDOFF = 0

CW = 1
CCW = 0

gpio.setmode(gpio.BCM)

gpio.setup(GPIO_DIR, gpio.OUT)
gpio.setup(GPIO_STEP, gpio.OUT)
gpio.setup(GPIO_DIR2, gpio.OUT)
gpio.setup(GPIO_STEP2, gpio.OUT)
gpio.setup(GPIO_LED, gpio.OUT)
gpio.setup(GPIO_IR, gpio.IN)

gpio.output(GPIO_DIR, CW)
gpio.output(GPIO_DIR2, CW)
gpio.output(GPIO_LED, LEDON)

print("Init")

def getBinary():
    # Internal vars
    num1s = 0  # Number of consecutive 1s read
    binary = 1  # The bianry value
    command = []  # The list to store pulse times in
    previousValue = 0  # The last value
    value = gpio.input(GPIO_IR)  # The current value

    # Waits for the sensor to pull GPIO_IR low
    while value:
        value = gpio.input(GPIO_IR)

    # Records start time
    startTime = datetime.now()

    while True:
        # If change detected in value
        if previousValue != value:
            now = datetime.now()
            pulseTime = now - startTime  # Calculate the time of pulse
            startTime = now  # Reset start time
            # Store recorded data
            command.append((previousValue, pulseTime.microseconds))

        # Updates consecutive 1s variable
        if value:
            num1s += 1
        else:
            num1s = 0

        # Breaks program when the amount of 1s surpasses 10000
        if num1s > 10000:
            break

        # Re-reads pin
        previousValue = value
        value = gpio.input(GPIO_IR)

    # Converts times to binary
    for (typ, tme) in command:
        if typ == 1:  # If looking at rest period
            if tme > 1000:  # If pulse greater than 1000us
                binary = binary * 10 + 1  # Must be 1
            else:
                binary *= 10  # Must be 0

    if len(str(binary)) > 34:  # Sometimes, there is some stray characters
        binary = int(str(binary)[:34])

    return binary

# Conver value to hex


def convertHex(binaryValue):
    tmpB2 = int(str(binaryValue), 2)  # Tempary propper base 2
    return hex(tmpB2)


def runCommand(cmd):
    global lastCommand
    
    print(cmd)
    
    if cmd == "PRESSED":        
        cmd = lastCommand
    
    lastCommand = cmd
    
    if cmd == "UP":
        gpio.output(GPIO_DIR, CW)
        for x in range(STEPS):
            gpio.output(GPIO_STEP, gpio.HIGH)
            sleep(PULSE)
            gpio.output(GPIO_STEP, gpio.LOW)
            sleep(PULSE)

    if cmd == "DOWN":
        gpio.output(GPIO_DIR, CCW)
        for x in range(STEPS):
            gpio.output(GPIO_STEP, gpio.HIGH)
            sleep(PULSE)
            gpio.output(GPIO_STEP, gpio.LOW)
            sleep(PULSE)
            
    if cmd == "RIGHT":
        gpio.output(GPIO_DIR2, CW)
        for x in range(STEPS):
            gpio.output(GPIO_STEP2, gpio.HIGH)
            sleep(PULSE)
            gpio.output(GPIO_STEP2, gpio.LOW)
            sleep(PULSE)

    if cmd == "LEFT":
        gpio.output(GPIO_DIR2, CCW)
        for x in range(STEPS):
            gpio.output(GPIO_STEP2, gpio.HIGH)
            sleep(PULSE)
            gpio.output(GPIO_STEP2, gpio.LOW)
            sleep(PULSE)


try:
    while True:
        # Runs subs to get incomming hex value
        inData = convertHex(getBinary())
        # print(inData)
        for button in range(len(Buttons)):  # Runs through every value in list
            if hex(Buttons[button]) == inData:  # Checks this against incomming
                runCommand(ButtonsNames[button])

# If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
except KeyboardInterrupt:
    print("Cleaning up!")
    gpio.cleanup()
