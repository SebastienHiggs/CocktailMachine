from flask import Flask, render_template, request
from time import time, sleep
import RPi.GPIO as GPIO

class Machine:
    def __init__(self):
        self.workingTillTime = 0
        self.bottles = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.pins = [7, 8, 10, 12, 11, 13, 15, 16, 19, 21, 22, 23]
        self.pourEndTimes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.setupGPIO()
    

    def setupGPIO(self):
        """Set up the GPIO pins"""
        GPIO.setmode(GPIO.BOARD)

        for pinNum in self.pins:
            GPIO.setup(pinNum, GPIO.OUT)


    def addBottleSeconds(self, bottle, seconds):
        """Adjust the end time for closing the pour for a bottle for a set amount of time in seconds
        
        bottle should be an integer from 0-11 selecting the ingredient bottle
        seconds should be a float of the amount of seconds to pour
        """
        self.pourEndTimes[bottle] = time() + seconds
        if self.pourEndTimes[bottle] > self.workingTillTime:
            self.workingTillTime = self.pourEndTimes[bottle]
    

    def openBottle(self, bottle):
        """Open the selected bottle by setting the GPIO pin to True"""
        GPIO.output(self.pins[bottle], True)
    

    def closeBottle(self, bottle):
        """Close the selected bottle by setting the GPIO pin to False"""
        GPIO.output(self.pins[bottle], False)
    

    def checkBottleOpen(self, bottle):
        """Return whether the selected GPIO pin is True or False"""
        GPIO.input(self.pins[bottle])
        

    def checkBottlesForClosing(self):
        """Check if any bottles should be closed due to time lapsed. Close them if appropriate"""
        for bottle in self.bottles:
            if self.checkBottleOpen(bottle):
                if self.pourEndTimes[bottle] < time():
                    self.closeBottle(bottle)


machine = Machine()


app = Flask(__name__)
print("1")
workingTillTime = 0
drinkLength = 5000
currentDrink = ""


# GPIO.output(pin[counter], True)        <- Start specific ingredient flow
# sleep(recipe[currentDrink][counter])   <- Wait x seconds
# GPIO.output(pin[counter], False)       <- Stop flow


@app.route('/', methods=['POST', 'GET'])
def main():
	"""try:
		_ = workingTillTime
	except UnboundLocalError:
		print("updating variables")
		workingTillTime = 0
		drinkLength = 5
	"""

	if request.method == 'POST':
		
		pythonTime = round(time()*1000)
		javascriptTime = int(str(request.data)[2:-1].split(",")[1])
		drinkID = str(str(request.data)[2:-1].split(",")[0])

		# Debugging time print statements
		print("Req Data: " + str(request.data)[2:-1])
		print("js: " + str(javascriptTime) + " py: " + str(pythonTime))
		print("Difference (js - py) = " + str(javascriptTime - pythonTime))
		
		if (javascriptTime > workingTillTime):
			print("Let's mix up drink:")
			print(drinkID)
			currentDrink = drinkID
			workingTillTime = javascriptTime + drinkTime(currentDrink)
			makeDrink(drinkID)
		else:
			print("Currently mixing drink " + str(currentDrink) + "... " + str(round(workingTillTime - javascriptTime, 2)) + " milliseconds left!")			
	return render_template('index.html')

if __name__	== "__main__":
	app.run(debug=True, host="0.0.0.0", port=80)

#If stuck in a stupid loop of not working type in localhost:80/index.html and it won't work but it seems to reset it somewhat
