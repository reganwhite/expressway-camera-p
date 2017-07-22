import cv2
import numpy as np

MAX_INT = 255

class sensor:
	"""Counts cars!"""
	def __init__(self, dim, lr1, frame):
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

		# Define the diff rate of the model
		self.dr		= 10	# Required difference for a car to exist (%)

		# Set our flags for whether or not a car exists
		self.flag = [ False, False, False, False ]

	def update(self, frame):
		"""Update the background intensity model."""
		self.truth = self.truth * (1 - self.lr1) + frame * self.lr1

	def compare(self, frame):
		"""Compares the input frame to the truth."""
		# Take the frame and find its average intensity for the four sections
		# Perform for both the truth and the new frame
		# Refresh the buffer
		self.flag = [ False, False, False, False ]

		for x in range(0,self.LANES):
			# Take the average of the lane section and append it to the buffer
			a = np.average(frame[x * self.h / 4, (x + 1) * self.h / 4])
			b = np.average(self.truth[x * self.h / 4, (x + 1) * self.h / 4])

			# Check to see if the two are sufficiently different then a car
			# exists.  Flag accordingly.
			if np.abs(((a - b) / b) * 100) >  self.dr:
				self.flag[x] = True

		self.update(frame)

	def run(self, frame):
		"""Main function called exteriorly by the handler."""
		# Perform the comparison
		cropFrame = frame[ 0:self.h, self.x:(self.x + self.w) ]
		self.compare(cropFrame)

		return self.retFlag()

	def retFlag(self):
		"""Return the current lane flags."""
		return self.flag
	
