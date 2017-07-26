import time
import cv2
import numpy as np
from ewc import ewc

MAX_INT = 255

class counter:
	"""Handler for sensor class."""
	def __init__(self,frame,param, loc):
		"""Initialize the handler."""
		# Import settings
		self.cfg = ewc()

		# Set the dimensions of the base frame
		self.height, self.width = frame.shape

		# Parse input params
		self.left	= param[0]
		self.right	= param[1]
		self.lr1	= param[2]

		# Define where we want the slices to be
		self.x = 0

		# Initialize lists to store sensor objects
		self.sensor_l = []
		self.sensor_r = []

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
			print "Left."
			self.sensor_l.append(sensor(self.x + (float(i) * float(self.width) / 10), 0.02, frame))
		for i in range(0, self.right):
			print "Right."
			self.sensor_r.append(sensor(self.width - (self.x + (float(i) * float(self.width) / 10)), 0.02, frame))

	def run(self, frame):
		"""Run the sensors. Takes a frame as input."""
		# Run the updater
		self.update(frame)

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

	def update(self, frame):
		"""Operates the sensor instances."""
		# Initialize storage for 
		statusLeft = []
		statusRight = []

		# Take the input frame and start comparisons
		for i in range(0, self.left):
			statusLeft.append(self.sensor_l[i].run(frame))
		for i in range(0, self.right):
			statusRight.append(self.sensor_r[i].run(frame))

		keypoints = []
		# Analyse output flags to see if things are working correctly.
		for i in range(0, self.left - 1):
			for j in range(0, 3):
				if self.sensor_l[i].flag[j]:
					keypoints.append(cv2.KeyPoint(self.sensor_l[i].x, (self.height / 8) + j * self.height / 4, 5))

		blankFrame = frame.copy()	# Make a copy of the frame so that we don't break it
		# Draw keypoints and number of features that we're tracking
		blankOut = cv2.drawKeypoints(blankFrame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
		cv2.imshow('Ping' + self.loc,blankOut)


class sensor:
	"""Counts cars!"""
	def __init__(self, dim, lr1, frame):
		"""Initialize the object."""
		# Set up constants the such
		self.h, self.w	= frame.shape	# Set the dimensions of the slice
		self.x		= int(dim)		# x location of the slice
		self.dr		= 15		# Required difference for a car to exist (%)
		self.lr1	= lr1		# Define the learning rate of the model
		self.LANES	= 4			# How many lanes are we looking at?
		
		# take the truth of the background
		self.truth	= frame[ 0:self.h, self.x:self.x + 1]
		
		# Set our flags for whether or not a car exists
		self.flag	= [ False, False, False, False ]

	def update(self, frame):
		"""Update the background-truth intensity model."""
		self.truth = self.truth * (1 - self.lr1) + frame * self.lr1

	####### ------- compare ------- #######
	# Compares the input frame to a historical model of the road.  If the average
	# pixel intensity in the input frame is sufficiently different to the historical
	# models average intensity, we assume that something is present.
	def compare(self, frame):
		"""Compares the input frame to the truth."""
		# Take the frame and find its average intensity for the four sections
		self.flag = [ False, False, False, False ] # Reset the buffer
		
		# Perform comparison between frame and truth
		for i in range(0,self.LANES):
			# Take the average of the lane section and append it to the buffer
			a = np.average(frame[i * self.h / 4 + self.h / 8:(i + 1) * self.h / 4 - self.h / 8])
			b = np.average(self.truth[i * self.h / 4 + self.h / 8:(i + 1) * self.h / 4 - self.h / 8])

			# Check to see if the two are sufficiently different.  If they are,
			# then set the flag as True.
			diff = np.abs(((a - b) / b) * 100)
			if diff > self.dr:
				self.flag[i] = True

		self.update(frame)

	def run(self, frame):
		"""Main function called exteriorly by the handler."""
		cropFrame = frame[ 0:self.h, self.x:self.x + 1] # Crop the frame
		self.compare(cropFrame) # Perform the comparison

		# Return the flags thrown by the comparison
		return self.retFlag()

	def retFlag(self):
		"""Return the current lane flags."""
		return self.flag
	
