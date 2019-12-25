from flask import Flask, render_template, request
from time import time, sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(7, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

pin = [7, 8, 10, 12, 11, 13, 15, 16, 19, 21, 22, 23]

app = Flask(__name__)
print("1")
workingTillTime = 0
drinkLength = 5000
currentDrink = ""

#Drink Recipe Array
#Recipe = [RecipeNo.][Bottle Amt]
#Amt of recipes, Amt of Bottles
recipe = {}
recipe["whiskey"] = [1,1,1,1,1,1,1,1,1,1,1,1]
recipe["1"] = [1,1,2,1,2,1,1,0,0,0,1,1]
recipe["2"] = [1,1,2,2,2,1,1,0,0,0,1,1]
recipe["3"] = [1,2,2,2,2,1,0,0,0,0,0,1]
recipe["4"] = [5,5,5,6,6,6,7,7,7,8,8,8]
recipe["5"] = [6,6,6,7,7,7,8,8,8,9,9,9]
recipe["6"] = [7,7,7,8,8,8,9,9,9,10,10,10]
recipe["7"] = [8,8,8,9,9,9,10,10,10,11,11,11]

#print(recipe)

print("2")

def makeDrink(currentDrink):
	print("In the thing")
	counter = 0
	print("DRINK::")
	print(currentDrink)
	while counter < 12:
		print(recipe[currentDrink][counter],"seconds of bottle No.",counter)
		GPIO.output(pin[counter], True)
		sleep(recipe[currentDrink][counter])
		GPIO.output(pin[counter], False)
		print("Done with Bottle No.",counter)
		counter = counter + 1

def drinkTime(currentDrink):
	counter2 = 0
	time = 0
	while counter2 < 12:
		 time = time + recipe[currentDrink][counter2]
		 counter2 = counter2 + 1
	print(time)
	time = time*1000
	return time

print("3")

def buttonClick(value, drinkLength):
	""""""

@app.route('/', methods=['POST', 'GET'])
def main():
	"""try:
		_ = workingTillTime
	except UnboundLocalError:
		print("updating variables")
		workingTillTime = 0
		drinkLength = 5
	"""
	global workingTillTime
	global currentDrink

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
