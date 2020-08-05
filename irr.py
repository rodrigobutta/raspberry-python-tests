import RPi.GPIO as GPIO
from datetime import datetime

# Button codes regarding test IR controller:
# Button Code - up: 0x300ff18e7
# Button Code - down: 0x300ff4ab5
# Button Code - right: 0x300ff5aa5
# Button Code - left: 0x300ff10ef
# Button Code - okk: 0x300ff38c7

pin = 17
Buttons = [0x300ff18e7, 0x300ff4ab5, 0x300ff5aa5, 0x300ff10ef, 0x300ff38c7, 0x3] 
ButtonsNames = ["UP", "DOWN", "RIGHT", "LEFT", "OK", "PRESSED"]

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN)

def getBinary():
	#Internal vars
	num1s = 0 #Number of consecutive 1s read
	binary = 1 #The bianry value
	command = [] #The list to store pulse times in
	previousValue = 0 #The last value
	value = GPIO.input(pin) #The current value
	
	#Waits for the sensor to pull pin low
	while value:
		value = GPIO.input(pin)
		
	#Records start time
	startTime = datetime.now()
	
	while True:
		#If change detected in value
		if previousValue != value:
			now = datetime.now()
			pulseTime = now - startTime #Calculate the time of pulse
			startTime = now #Reset start time
			command.append((previousValue, pulseTime.microseconds)) #Store recorded data
			
		#Updates consecutive 1s variable
		if value:
			num1s += 1
		else:
			num1s = 0
		
		#Breaks program when the amount of 1s surpasses 10000
		if num1s > 10000:
			break
			
		#Re-reads pin
		previousValue = value
		value = GPIO.input(pin)
		
	#Converts times to binary
	for (typ, tme) in command:
		if typ == 1: #If looking at rest period
			if tme > 1000: #If pulse greater than 1000us
				binary = binary *10 +1 #Must be 1
			else:
				binary *= 10 #Must be 0
			
	if len(str(binary)) > 34: #Sometimes, there is some stray characters
		binary = int(str(binary)[:34])
		
	return binary
	
#Conver value to hex
def convertHex(binaryValue):
	tmpB2 = int(str(binaryValue),2) #Tempary propper base 2
	return hex(tmpB2)
	
while True:
	inData = convertHex(getBinary()) #Runs subs to get incomming hex value
	#print(inData)
	for button in range(len(Buttons)):#Runs through every value in list
		if hex(Buttons[button]) == inData: #Checks this against incomming
			print(ButtonsNames[button]) #Prints corresponding english name for button
    