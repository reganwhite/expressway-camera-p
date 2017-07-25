import cv2
import numpy as np
import math
# Base video input resolution
DEF_RES_W				= 1920
DEF_RES_H				= 1080
IM_BIN_SIZE				= 4

_X1						= 0
_X2						= 1360
_Y1						= 0
_Y2						= 1080
_W						= np.int(np.ceil((_X2 - _X1) / IM_BIN_SIZE))
_H						= np.int(np.ceil((_Y2 - _Y1) / IM_BIN_SIZE))

# Gaussian Blur
GAUSS_KSIZE				= 3
GAUSS_SIGMA_X			= 0
GAUSS_SIGMA_Y			= 0


class adjuster:
	"""Takes a frame input and returns an adjusted version for use in the expresswayTracker class."""

	def __init__(self):
		"""Initialiszes the function"""
		# Set the coordinates of the rectangle where the road lies
		self._X		= 0
		self._Y		= 0
		self._W		= 1920
		self._H		= 1080

		# Set the Y coordinate marking the centre of the road, to split the image
		self.inboundHeight	= 422

		# Set the downsample factor
		self.down		= IM_BIN_SIZE

	def adjust(self, frame, crop = True, resize = True, cvt = True):
		"""Performs intiial transformations on the frame to make it more suitable for work.
		Takes an input of a frame."""
		# Do some transforms.  Do in the following order because this is the fastest way
		#	1. Crop
		#	2. Resize
		#	3. RGB -> Greyscale
		#	4. Blur
		if crop:
			frame = frame[_Y1:_Y2, _X1:_X2]
		if resize:
			frame = cv2.resize(frame,(_W, _H),0,0,cv2.INTER_LINEAR)	# Resize the frame to make it more manageable - INTER_LINEAR because it's fast
		if cvt:
			frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)			# Convert RGB to Grayscale
		#frame = cv2.GaussianBlur(frame, (GAUSS_KSIZE, GAUSS_KSIZE), 0)	# Perform Gaussian Blur to make things run a bit easier

		# Split the road into top/bottom
		sizeX, sizeY = frame.shape[:2]
		frameTop = frame[0:self.inboundHeight / self.down - 1, 0:sizeX]
		frameBot = frame[self.inboundHeight / self.down:sizeY, 0:sizeX]

		return frameTop, frameBot
