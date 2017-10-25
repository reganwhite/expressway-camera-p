import time
import cv2
import numpy as np
from threading import Thread
import requests
import math
import datetime


class timer:
	"""This is a timer used to check how things are running!  Operates over a fixed number of iterations."""
	def __init__(self, ITERATIONS = 1000, NAME = "BLNK", DISP_RPS = False, DISP_TIME = False, DISP_PERC = False, ROOT = False, USE = True, WRITE = False):
		self.USE = USE
		if self.USE:
			# Parse inputs
			self.NAME = NAME				# What do we want to name this instance?
			self.DISP_RPS = DISP_RPS		# Do we want to display the output to console?
			self.DISP_TIME = DISP_TIME		# Do we want to display the output to console?
			self.DISP_PERC = DISP_PERC		# Do we want to display the output to console?
			self.ITERATIONS = ITERATIONS	# How many iterations are we expecting the tik to average over?
			self.ROOT = ROOT				# Is this the base timer?
			self.WRITE = WRITE

			if self.WRITE:
				self.file = open("E:/ewc-debug/" + self.NAME + ".txt", "a")
				self.file.write("------------------------------------------------\n")
				string = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
				self.file.write("Time: " + string + "\n")
				self.file.write("Starting new test for:\n")
				self.file.write(self.NAME + "\n")
				self.file.write("TIME (s)\n")

			# Set up name for display
			self.NAME_FIX = "[" + self.NAME

			# Initialize timers
			self.t1 = 0
			self.t2 = 0
			self.t_tik = 0

			# Initialize counter
			self.count = 0

	def end(self):
		if self.WRITE:
			self.file.close()

	def tik(self):
		"""Starts the counter."""
		if self.USE:
			tik = self.t1
			self.t1 = time.time()
			if self.count > 0:
				self.t_tik += self.t1 - tik

	def tok(self):
		"""Closes the tok and does some things"""
		if self.USE:
			self.count += 1
			self.t2 += float(time.time()) - float(self.t1)

			if self.count == self.ITERATIONS:
				if self.ROOT:
					print("------------------------------------------------")
				if self.DISP_RPS:
					# Print the output to console
					if self.t2 != 0:
						print('\r{0:>12}] = {1:11.4f} /s'.format(self.NAME_FIX, self.ITERATIONS/(self.t2)))
					else:
						print('\r{0:>12}] = {1:>12s}'.format(self.NAME_FIX, "undef/s"))
				if self.DISP_TIME:
					# Print the output to console
					if self.t2 != 0:
						print('\r{0:>12}] = {1:11.4f} s'.format(self.NAME_FIX, float(self.t2) / float(self.ITERATIONS) ))
						
					else:
						print('\r{0:>12}] = {1:>12s}'.format(self.NAME_FIX, "undef s"))
				if self.DISP_PERC:
					if self.t2 != 0:
						print('\r{0:>12}] = {1:11.4f} %'.format(self.NAME_FIX, float(self.t2) / float(self.t_tik) * 100))
					else:
						print('\r{0:>12}] = {1:>12s} %'.format(self.NAME_FIX, "0"))

				if self.WRITE:
					write = []
					if self.DISP_TIME:
						write.append(str(float(self.t2) / float(self.ITERATIONS)))
					else:
						write.append("-")
					#if self.DISP_PERC:
					#	write.append(str(float(self.t2) / float(self.t_tik) * 100))
					#else:
					#	write.append("-")
					#if self.DISP_RPS:
					#	write.append(str(self.ITERATIONS / self.t2))
					#else:
					#	write.append("-")

					string = "	".join(write)
					self.file.write(string + "\n")
				
				# Reset everything
				self.count	= 0
				self.t2		= 0
				self.t_tik	= 0


class adjuster:
	"""Takes a frame input and returns an adjusted version for use in the expresswayTracker class."""

	def __init__(self,settings):
		"""Initialiszes the function"""
		# Import settings
		self.cfg = settings

		# Set the Y coordinate marking the centre of the road, to split the image
		self.inboundHeight	= 422

	def adjust(self, frame, crop = True, resize = True, cvt = True, fromFile = True):
		"""Performs intiial transformations on the frame to make it more suitable for work.
		Takes an input of a frame."""
		# Do some transforms.  Do in the following order because this is the fastest way
		#	1. Crop
		#	2. Resize
		#	3. RGB -> Greyscale
		#	4. Blur
		intCrop = int(220 / float(480/self.cfg._FG_HEIGHT))

		if crop:
			frame = frame[self.cfg._Y1:self.cfg._Y2, self.cfg._X1:self.cfg._X2]
		if resize:
			frame = cv2.resize(frame,(self.cfg._W, self.cfg._H),0,0,cv2.INTER_LINEAR)	# Resize the frame to make it more manageable - INTER_LINEAR because it's fast
		if cvt:
			frame = frame.astype(np.uint8)
			frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)			# Convert RGB to Grayscale
		if self.cfg.GAUSS_KSIZE != 0:
			frame = cv2.GaussianBlur(frame, (self.cfg.GAUSS_KSIZE, self.cfg.GAUSS_KSIZE), 0)	# Perform Gaussian Blur to make things run a bit easier
		if fromFile:
			# Split the road into top/bottom
			sizeX, sizeY = frame.shape[:2]
			frameTop = frame[0:self.inboundHeight / self.cfg.IM_BIN_SIZE - 1, 0:sizeX]
			frameBot = frame[self.inboundHeight / self.cfg.IM_BIN_SIZE:sizeY, 0:sizeX]
		else:
			# Split the road into top/bottom
			sizeX, sizeY = frame.shape[:2]
			frameTop = frame[0:intCrop, 0:sizeX]
			frameBot = frame[intCrop + 1:sizeY, 0:sizeX]

		return frameTop, frameBot


class requester:
	"""HTTP Request Class: This class is used to transfer data from the system to the web server via HTTP requests."""

	def __init__(self, urlP1, target):
		"""Initialize the class information."""
		# URL of Data Handler for Average Speed
		self.urlPost1 = urlP1

		# OTHER URLS
		self.target = target

		# Initialize Variables for Speed
		self.speedRawComb = []
		self.speedAvgComb = []
		self.speedAvgUNIX = []
		self.speedStrComb = ''
		self.speedStrUNIX = ''

		# Initialize Variables for Lane-By-Lane data
		self.speedRawLane = [0, 0, 0, 0]
		self.speedAvgLane = []
		self.speedStrLane = ''

		# Initialize other random stuff
		self.rawDataGap = []
		self.stringDataGap = ''

		self.ts_write_key	= "1M1BZ89RA33RT2NF"
		self.ts_read_key	= "IKS43FIAIA50VY9O"
		self.ts_update_url= "https://api.thingspeak.com/update"


	def dataAppend(self, avgTotalSpeed, avgLaneSpeed, type):
		"""Appends newest data to the end of the buffer."""
		# Take the latest speed input and appends to the raw buffer
		self.speedRawComb.append(avgTotalSpeed)
		self.speedRawLane = [i + j for i, j in zip(self.speedRawLane, avgLaneSpeed)]

		# If there are 100 values in the list:
		#	1. Take the avearge of all values in the list
		#	2. Append this average value to another list
		if len(self.speedRawComb) == 100:
			# Average Total
			self.speedAvgComb.append(sum(self.speedRawComb)/len(self.speedRawComb))
			self.speedRawComb = []

			# Average Lane
			self.speedAvgLane.append([float(x) / 100 for x in self.speedRawLane])
			self.speedRawLane = [0, 0, 0, 0]

			# Time Stamp
			self.speedAvgUNIX.append(time.time() + 10 * 60 * 60)

			# If there are 4 values in the list:
			if len(self.speedAvgComb) == 4:
				# Create strings for sending
				self.postMaker()

				# Start thread for requester
				self.startPoster()

				# Tidy up afterwards
				self.speedAvgComb = []
				self.speedAvgLane = []
				self.speedAvgUNIX = []
			
	def postMaker(self):
		"""Posts information to the specified URL."""
		# Exmpy the strings before we start appending
		self.speedStrComb = ''
		self.speedStrUNIX = ''
		self.speedStrLane = ''

		# For each element in the array
		for i in range(0,4):
			# Append data as string
			self.speedStrComb = self.speedStrComb + str(self.speedAvgComb[i])
			self.speedStrUNIX = self.speedStrUNIX + str(self.speedAvgUNIX[i])
			self.speedStrLane = self.speedStrLane + "|".join(str(a) for a in self.speedAvgLane[i])
			
			if i < 3:
				# Add comma delmiter
				self.speedStrComb = self.speedStrComb + ","
				self.speedStrUNIX = self.speedStrUNIX + ","
				self.speedStrLane = self.speedStrLane + ","

	def poster(self):
		"""Posts information to web-server at specified URL."""
		# Perform HTTP request
		r = requests.get(self.urlPost1, params = {'sp':self.speedStrComb, 't':self.speedStrUNIX, 'l':self.speedStrLane, 'dir':self.target})
		return
	
	def startPoster(self):
		"""Starts thread for data poster."""
		# Start thread for Poster
		Thread(target = self.poster, args = ()).start()

		return self

	def sendSpeed(self, speed, sendtime, speedLane, target):
		"""Posts information to web-server at specified URL."""
		# Perform HTTP request
		print(speed)
		r = requests.get(self.urlPost1, params = {'sp':speed, 't':sendtime, 'l':speedLane, 'dir':target})
		return

	def startSendSpeed(self, speed, sendtime, speedLane, target):
		"""Starts thread for data poster."""
		# Start thread for Poster
		Thread(target = self.sendSpeed, args = (speed, sendtime, speedLane, self.target)).start()

		return self

	def ts_poster(self):
		"""Posts information to the thingspeak channel."""
		r = requests.get(self.ts_update_url, params = {'api_key':self.speedStrComb, 'field1':self.speedStrUNIX, 'field1':self.speedStrLane})
