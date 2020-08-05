import RPi.GPIO as GPIO
import time 

print("Starting led 6...")

GPIO.setmode(GPIO.BCM)

GPIO.setup(24, GPIO.OUT)

GPIO.output(24, GPIO.HIGH)

time.sleep(8)

GPIO.output(24, GPIO.LOW)

GPIO.cleanup()

print("Finishing led..")