import time
import cv2
import numpy as np
from ewctools import timer

MAX_INT = 255

class counter:
	"""Handler for sensor class."""
	def __init__(self, frame, settings, loc, left = 2, right = 2, LR = 0.02):
		"""Initialize the handler."""
		# Set the dimensions of the base frame
		self.height, self.width = frame.shape

		# Import the settings
		self.cfg = settings

		# Counter to keep track of how many frames we've processed
		self.count = 0

		# Sensor initialisation parameters
		self.LANES = 4		# pretty self explanatory
		self.SPACE = 20		# factor of total width that the sensors should be spaced apart
		self.OFFSET = 10	# offset that the sensors need to be from the sides of then frame

		# Counter for the number of cars counted
		self.carCounter = [0,0]

		# Parse input params
		self.left	= left
		self.right	= right
		self.LR1	= LR
		self.LR1_BASE	= LR
		self.LR1_UPDATE = False
		self.FILTER_SPEED = 30

		# Define where we want the slices to be

		# Initialize lists to store sensor objects
		self.sensor_l = []
		self.sensor_r = []

		# Historical Flags
		self.histLeft = []
		self.hisRight = []

		# Set up flags to store the ready status of different components
		self.readyStatusL = False
		self.readyStatusR = False
		self.runStatus = True

		# Set up storage for input frames
		self.frameBuffer = frame.copy()
		self.frameInUse = frame.copy()

		# Is this the top or bottom traffic?
		self.loc = " " + loc

		# Populate the lists with instances of "sensor"
		for i in range(0, self.left):
			self.sensor_l.append(sensor(self.OFFSET + (float(i) * float(self.width) / self.SPACE), self.LR1, frame))
		for i in range(0, self.right):
			self.sensor_r.append(sensor(self.width - (self.OFFSET + (float(i) * float(self.width) / self.SPACE)), self.LR1, frame))

		# Initialise a couple of timers to test things our
		self.timer1 = timer(NAME = loc + "-CNT-RUN", USE = False)
		self.timer2 = timer(NAME = loc + "-CNT-CMP", USE = False)


	def run(self, frame, SPEED = False):
		"""Run the sensors. Takes a frame as input."""
		# Run the updater
		self.count(frame, SPEED)
		return self.carCounter

	def push(self, frame):
		"""Pushes the latest frame to the object."""
		# Push the latest frame to buffer
		self.frameBuffer = frame.copy()

		# Set the status flag to ready
		self.readyStatus = True

	def getStatus(self):
		"""Returns the runtime status of the counter."""
		return self.readyStatus

	def setStatus(self, status):
		"""Sets the run status of the module to the input."""
		self.runStatus = status

	def updateLEARN(self, SPEED):
		if SPEED != False:
			if SPEED >= 0:
				self.LR1_UPDATE = True
				if SPEED > self.FILTER_SPEED:
					SPEED = self.FILTER_SPEED
				self.LR1 = self.LR1_BASE * (float(self.FILTER_SPEED) / float(SPEED))

	def count(self, frame, SPEED = False):
		"""Operates the sensor instances."""
		# Update the counter
		self.count += 1

		if SPEED != False:
			self.updateLEARN(SPEED)

		# Initialize storage for 
		statusLeft = []
		statusRight = []

		self.timer1.tik()
		# Run the sensors given the input frame
		for i in range(0, self.left):
			if self.LR1_UPDATE == True:
				self.sensor_l[i].updateLEARN(self.LR1)
			statusLeft.append(self.sensor_l[i].run(frame))
		for i in range(0, self.right):
			if self.LR1_UPDATE == True:
				self.sensor_r[i].updateLEARN(self.LR1)
			statusRight.append(self.sensor_r[i].run(frame))
		self.timer1.tok()
		self.timer2.tik()
		if self.LR1_UPDATE == True:
			self.LR1_UPDATE = False

		# If the sensor has been running for a sufficient amount of time
		if self.count > 100:
			for i in range(0, self.LANES):
				for j in range(0, self.left):
				# Sensors on the left of frame
					if self.histLeft[j][i] == True:
						if statusLeft[j][i] == False:
							self.carCounter[0] += float(1) / float(self.left)	# Looks like we found a car, increment counter
				for j in range(0, self.right):
				# Sensors on the right of frame
					if self.histRight[j][i] == True:
						if statusRight[j][i] == False:
							self.carCounter[1] += float(1) / float(self.right)	# Looks like we found a car, increment counter
		self.timer2.tok()
		# Update the historical flags
		self.histLeft	= statusLeft[:]
		self.histRight	= statusRight[:]
		

		keypoints = []
		# Analyse output flags to see if things are working correctly.
		for i in range(0, self.left):
			for j in range(0, self.LANES):
				if self.sensor_l[i].flag[j]:
					keypoints.append(cv2.KeyPoint(self.sensor_l[i].OFFSET, (self.height / 8) + j * self.height / 4, 5))

		for i in range(0, self.right):
			for j in range(0, self.LANES):
				if self.sensor_r[i].flag[j]:
					keypoints.append(cv2.KeyPoint(self.sensor_r[i].OFFSET, (self.height / 8) + j * self.height / 4, 5))

		blankFrame = frame.copy()	# Make a copy of the frame so that we don't break it
		# Draw keypoints and number of features that we're tracking
		blankOut = cv2.drawKeypoints(blankFrame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
		cv2.imshow('Ping' + self.loc,blankOut)


###### ------- sensor ------- ######
# Class used by counter.  Monitors a vertical slice covering all lanes of the road, and throws flags
# depending on whether or not a car is detected on the slice within a lane.
class sensor:
	"""Counts cars!"""
	def __init__(self, OFFSET, LR1, frame, CHECK_SIZE_FACTOR = 24, LANES = 4, DIFFERENCE = 30, THICKNESS = 1):
		"""Initialize the object."""
		# Set up constants the such
		self.h, self.w = frame.shape	# Set the dimensions of the slice
		self.OFFSET	= int(OFFSET)		# x location of the slice
		self.DIFFERENCE	= DIFFERENCE	# Required difference for a car to exist (%)
		self.LR1 = LR1					# Define the learning rate of the model
		self.LANES = LANES				# How many lanes are we looking at?
		self.CHECK_SIZE_FACTOR = CHECK_SIZE_FACTOR	# What factor of the frame height are we going to check the difference of?
		self.THICKNESS = THICKNESS		# How thick do we want the slice to be?

		# Initialize counter
		self.count	= 0
		
		# take the truth of the background
		self.truth	= frame[ 0:self.h, self.OFFSET:self.OFFSET + 1]
		
		# Set our flags for whether or not a car exists
		self.flag		= [ False, False, False, False ]
		self.flag_cnt	= [ 0, 0, 0, 0 ]

		self.bounced = []
		for i in range(0,self.LANES):
			self.bounced.append(bounce())

	def update(self, frame):
		"""Update the background-truth intensity model."""
		self.truth = self.truth * (1 - self.LR1) + frame * self.LR1

	####### ------- compare ------- #######
	# Compares the input frame to a historical model of the road.  If the average
	# pixel intensity in the input frame is sufficiently different to the historical
	# models average intensity, we assume that something is present.
	def compare(self, frame):
		"""Compares the input frame to the truth."""
		# Increment counter
		self.count += 1

		# Take the frame and find its average intensity for the four sections
		self.flag = [ False, False, False, False ] # Reset the buffer
		
		# Perform comparison between frame and truth
		for i in range(0,self.LANES):
			# Take the average of the lane section and append it to the buffer
			a = np.average(frame[i * self.h / self.LANES + self.h / (self.LANES * 2) - self.h / self.CHECK_SIZE_FACTOR:i * self.h / self.LANES + self.h / (self.LANES * 2) + self.h / self.CHECK_SIZE_FACTOR])
			b = np.average(self.truth[i * self.h / self.LANES + self.h / (self.LANES * 2) - self.h / self.CHECK_SIZE_FACTOR:i * self.h / self.LANES + self.h / (self.LANES * 2) + self.h / self.CHECK_SIZE_FACTOR])
			
			# Check to see if the two are sufficiently different.  If they are,
			# then set the flag as True.
			diff = np.abs(((a - b) / b) * 100)
			if diff > self.DIFFERENCE:
				self.flag[i] = True

		# Update the truth for the next frame
		self.update(frame)

	def run(self, frame, frametime = False):
		"""Main function called exteriorly by the handler."""
		cropFrame = frame[ 0:self.h, self.OFFSET:self.OFFSET + 1] # Crop the frame
		self.compare(cropFrame) # Perform the comparison

		# Return the flags thrown by the comparison
		return self.retFlag(frametime)

	def retFlag(self, frametime = False):
		"""Return the current lane flags."""
		# Compare the current frames flags to the previous frames flags
		outcome = []
		for i in range(0, self.LANES):
			outcome.append(self.bounced[i].run(self.flag[i], frametime))

		return outcome

	def updateLEARN(self, LR):
		"""Update the sensor learning rate from input."""
		self.LR1 = LR
	

###### ------- bounce ------- ######
# Small class used by the sensor class.  Monitors the stability of flag changes, to prevent flickering
# from affecting the vehicle count.
class bounce:
	"""Debounces flags.  Prevents flags appearing and disappearing, and triggering the counter."""
	def __init__(self, THRESHOLD = 3):
		"""Initialise variables."""
		# Initialise variables
		self.curr = False	# current sensor state
		self.good = 0		# number of good comparisons
		self.fail = 0		# number of bad comparisons
		self.THRESHOLD = THRESHOLD

		self.timeTrue = 0
		self.timeFalse = 0

		self.timePass = 0

	def returnTime (self):
		"""Returns the time it took the vehicle to throw two consecutive flags."""
		return self.timePass

	def run(self,bool, frametime = False):
		"""Takes a boolean input, and checks against historic inputs for stability.  Returns current state."""
		if bool != self.curr:
		# input is different to current state
			self.fail += 1	# increment bad comparison
			if self.fail > self.THRESHOLD:
			# number of bad comparisons has passed threshold, switching state
				if not frametime:
				# if the system is running in real time
					# Take note of the time that the switch has occured at
					if self.curr == False:
						self.timeFalse = time.time()
					else:
						self.timeTrue = time.time()
				else:
				# if we are using pre-recorded frame times
					# Take note of the time that the switch has occured at given the input time
					if self.curr == False:
						self.timeFalse = frametime
					else:
						self.timeTrue = frametime

				# calculate the amount of time it took the vehicle to pass the threshold
				# if timePass is +ve, then gap duration
				# if			 -ve, then pass duration
				self.timePass = self.timeFalse - self.timeTrue

				self.curr = not self.curr	# switch state
				
				# reset counters
				self.fail = 0
				self.good = 0

		else:
		# input is the same as current state
			self.good += 1
			if self.good > self.THRESHOLD:
			# input has been consistently good, reset counters
				self.fail = 0
				self.good = 0

		return self.curr