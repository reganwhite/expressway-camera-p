import cv2
import numpy as np

MAX_INT = 255

class sensor:
	"""Counts cars!"""
	
	def __init__(self,dim,lr1,frame):
		"""Initialize the object."""
		# Set the dimensions of the slice
		self.h, self.w	= frame.shape
		self.x			= dim

		# How many lanes are we looking at?
		self.LANES = 4

		# take the truth of the background
		self.truth = frame[ 0:self.h, self.x:(self.x + self.w)]

		# Define the learning rate of the model
		self.lr1	= lr1

		# Set our flags for whether or not a car exists
		self.flag = [ False, False, False, False ]


	def start(self):
		"""Starts the different tracks of the counter"""


	def update(self,frame):
		"""Update the background intensity model."""
		self.truth = self.truth * (1 - self.lr1) + frame * self.lr1

	def compare(self,frame):
		"""Compares the input frame to the truth."""
		# Get the difference between the two frames
		comp = abs(self.truth - frame)

		# Perform the threshold
		ret, compThresh = cv2.threshold(comp, 10, MAX_INT, cv2.THRESH_BINARY)

		# We have 4 lanes, so separate into them
		for x in range(0,self.LANES):
			# Check to see if a car exists in that region
			# Get the intensities
			for y in range(x * self.h / 4, (x + 1) * self.h / 4):
				# Increment the cumulative sum
				cumSum += compThresh[y]

			# Get the average intensities
			avgInt = cumSum / self.h / self.LANES

			# If a number of the pixels in the scene throw a flag, there is a car there.
			if avgInt >= (self.h / self.LANES) * MAX_INT / 4:
				# set the flag to true
				self.flag[x] = True
			else:
				# set the flag to false
				self.flag[x] = Flase

		self.update(frame)

	def ticker(self,frame):
		"""Main function called exteriorly by the handler."""
		# Perform the comparison
		self.compare(frame)

		return self.retFlag()

	def retFlag(self):
		"""Return the current lane flags."""
		return self.flag
	
