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
        
        'bottle' should be an integer from 0-11 selecting the ingredient bottle
        'seconds' should be a float of the amount of seconds to pour
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
        return GPIO.input(self.pins[bottle])
        

    def checkBottlesForClosing(self):
        """Check if any bottles should be closed due to time lapsed. Close them if appropriate.
        
        Return True if not finished, return False if finished."""

        stillGoing = False

        for bottle in self.bottles:
            if self.checkBottleOpen(bottle):
                stillGoing = True
                if self.pourEndTimes[bottle] < time():
                    self.closeBottle(bottle)
        
        return stillGoing

    def startRecipe(self, recipe):
        """Start pouring drinks appropriately for the given recipe.
        
        It should open the appropriate bottles, then set the times they should close.
        'recipe' should be a length-12 list of floats denoting the amount of seconds necessary per bottle.
        """
        for bottle in self.bottles:
            pourTime = recipe[bottle]
            if pourTime > 0:
                self.addBottleSeconds(bottle, pourTime)
                self.openBottle(bottle)


# Initialising the machine class instance
machine = Machine()

# Writing down the recipes (in seconds per bottle)
recipes = {"1": [1,2,3,4,5,6,7,8,9,10,11,12],
           "2": [1,1,1,1,1,1,3,3,3,3,3,3],
           "3": [0,0,0,0,0,0,0,0,0,0,2,2],
           "4": [1,2,3,1,2,3,1,2,3,0,0,4.0243]}

# Initialising Flask
app = Flask(__name__)

# This is a decorator that makes the main() function a Flask function - it can run a website.
@app.route('/', methods=['POST', 'GET'])
def main(): # This is what's called when the page is searched for
    
    # This checks for information coming from the page in the form of a post request.
    if request.method == 'POST':
        
        # Finding the times both this script and the web page are reporting
        pythonTime = round(time()*1000)
        javascriptTime = int(str(request.data)[2:-1].split(",")[1])

        # Getting the info of what drink the user wants!
        drinkID = str(str(request.data)[2:-1].split(",")[0])

        # Printing the received data
        print("Req Data: " + str(request.data)[2:-1])

        # Printing out both this script's and the webpage's reported times
        print("py: " + str(pythonTime) + " js: " + str(javascriptTime))
        print("Difference (py - js) = " + str(pythonTime - javascriptTime))

        if (javascriptTime > machine.workingTillTime and False): #Remove this 'False'!
            print("Let's mix up a drink: ")
            print(drinkID)
            machine.startRecipe(recipes[drinkID])
            
            print("recipe started!")
            print("Are the bottles all closed? " + str(machine.checkBottlesForClosing()))

            # This continuously checks whether bottles should be closed, and returns false if they're all closed.
            while machine.checkBottlesForClosing():
                # Sleep a little to allow the pi to do things other than a really fast loop.
                # I think not doing this is what caused an earlier version to crash.
                print("presleep")
                sleep(0.3) # <-- CHANGE THIS! It's too high a number atm (for testing), maybe put 0.05?

                # Debugging statements
                print("\nTest iteration. Still not finished!")
                print("Now: " + str(time()) + " || End times: " + str(machine.pourEndTimes))
                print([["Closed", "Open"][machine.checkBottleOpen(bottle)] for bottle in machine.bottles])
            print("Drink finished pouring!")
        else:
            print("Currently mixing a drink! ")
        print("Last req method statement")
    print("pre-return")
    return render_template('index.html')

if __name__    == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)

print("End of file!")
#If stuck in a stupid loop of not working type in localhost:80/index.html and it won't work but it seems to reset it somewhat
