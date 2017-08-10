# Declare the different libraries and what not that we might need
import numpy as np
import cv2
import time
import math
from ewctools import requester
import string
import random
import matplotlib.pyplot as plt
from ewctools import timer


# Define some flags
SV_USE_DEBUG			= True
SV_FILTER_KEYPOINTS		= True
SV_DEMO					= False		# FLAG FOR PROJECT DEMONSTRATION
SV_RUN_LIVE				= False
SV_SEND_DATA			= True

####### ------- COMPONENT SETTINGS ------- #######
# Note that some of the settings may be deprecated and no longer in use.
# They remain listed for posterity, as how the class functions is subject to
# change.

# Start Delay
SV_START_DELAY			= 100		# number of frames the sytem will process before commencing analysis
SV_SEND_DELAY			= 1000		# number of frames the system will process before sending to server

# FAST (Fast Feature Detector)
FFD_THRESHOLD			= 66
				# Can incremement this with fast.setThreshold

# Descriptor Extractor
ORB_NFEATURES			= 1
ORB_SCALEFACTOR			= 1
ORB_NLEVELS				= 1
ORB_EDGETHRESH			= 3
ORB_FIRSTLEVEL			= ORB_EDGETHRESH
ORB_WTA_K				= 3
ORB_SCORETYPE			= cv2.ORB_FAST_SCORE

# Base video input resolution
DEF_RES_W				= 1920
DEF_RES_H				= 1080
IM_BIN_SIZE				= 4

# Define other useful variables
_LR1					= 0.1			# Learning rate for keypoint remover
_LR1_BASE				= 0.1
_LR2					= 0.01			# Learning rate for Speed Updater
_LR2_BASE				= 0.01
_X1						= 1
_X2						= 1360
_Y1						= 1
_Y2						= 1080
_W						= np.int(np.ceil((_X2 - _X1 + 1) / IM_BIN_SIZE))
_H						= np.int(np.ceil((_Y2 - _Y1 + 1) / IM_BIN_SIZE))
_FPS					= float(20)			# FPS of video file if being read from a video
_PPM_UNSCALED			= 195
_PPM					= float( _PPM_UNSCALED / IM_BIN_SIZE / 3)	# Number of Pixels-Per-Meter
_MPS_to_KPH				= float(3.6)				# constant
_PixDiff				= 0.05
_FILTER_SPEED			= 30						# max concernable filter speed in kph



####### ------- EXPRESSWAY TRACKER MK.2 ------- #######
class tracker:
	"""Class used to track vehicles."""

	def __init__(self, loc, frameInit):
		"""Initialize things."""
		# Initialise the requester
		if loc == "Top":
			_PPM_UNSCALED = 205
		else:
			_PPM_UNSCALED = 170
			
		self.requester = requester('http://regandwhite.com/traffic/data/entry.php', loc)
		_PPM = float( _PPM_UNSCALED / IM_BIN_SIZE / 3)
		self.loc = " " + loc

		# Make the fast corner detector
		self.fast = cv2.FastFeatureDetector_create(FFD_THRESHOLD)

		# Buffer of different kernals for transforms
		self.kernel1 = np.ones((2,2),np.uint8)
		self.kernel2 = np.ones((6,6),np.uint8)

		# Start a counter so we can see how many iterations we've been through
		self.count = 0
		self.height, self.width = frameInit.shape
		self.LANES = 4

		# Initialize the dot matrix
		self.baseFrame = frameInit.copy()
		self.baseFrame[:] = 0
		
		# Descriptor Extractors
		self.descExtractor1 = cv2.ORB_create(edgeThreshold = ORB_EDGETHRESH, patchSize = ORB_EDGETHRESH,
											WTA_K = ORB_WTA_K, scoreType = ORB_SCORETYPE)

		# Point Matcher
		self.descBruteForce = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck = False)
		cv2.BFMatcher
		FLANN_INDEX_LSH = 6
		ip = dict(algorithm = FLANN_INDEX_LSH, table_number = 6, key_size = 12, multi_probe_level = 1)
		sp = dict(checks = 10)

		self.descFlannMatch = cv2.FlannBasedMatcher(indexParams = ip, searchParams = sp)

		# Get a storage point ready for the previous frame
		self.oldFrame = self.baseFrame
		self.oldKeypoints = []
		self.oldDescripts = []
		self.oldSortedDSC = [[],[],[],[]]

		# Compute instances
		self.sortedKey = [[],[],[],[]]
		self.sortedDsc = [[],[],[],[]]
		self.compute = []
		for i in range(0,self.LANES):
			self.compute.append(trackerCompute(LANES = 4, LANE = i))
		self.computeSingle = trackerCompute(LANES = 1, LANE = 1, LOC = loc)


		# set up some timers
		self.timeStart = time.time()
		self.timeFinish = time.time()
		self.timerMatch = timer(USE = False, ITERATIONS = 200, DISP_RPS = True, DISP_PERC = False, NAME = loc + "-STAND", ROOT = True, WRITE = True, DISP_TIME = True)
		self.timerBrute = timer(USE = False, ITERATIONS = 200, DISP_RPS = True, DISP_PERC = False, NAME = loc + "-MULTI", WRITE = True, DISP_TIME = True)
		self.timerRadiu = timer(USE = False, ITERATIONS = 200, DISP_RPS = True, DISP_PERC = False, NAME = loc + "-CLASS", DISP_TIME = True)
		
		self.timerTRACK = timer(ITERATIONS = 200, DISP_RPS = True, DISP_PERC = False, NAME = loc + "-TRACK", ROOT = True, DISP_TIME = True)


		# Values for the running of the system
		self.firstCount	  = True		# Check for first time that the matche checker is run

		self.averageSpeed = 0			# weighted average speed of vehicles
		self.averageFrame = 9999		# weighted average pixel speed of vehicles
		self.currentSpeed = 0			# current speed of vehicles
		self.currentFrame = 9999		# current pixel speed of vehicles

		self.currentLaneSpeed = [ 0, 0, 0, 0 ]
		self.averageLaneSpeed = [ 0, 0, 0, 0 ]

		self.LANES = 4

		if loc == "Top":
			_PPM = float(178)
		else:
			_PPM = float(205)

		_PPM = float( _PPM / IM_BIN_SIZE / 3)

		self.readyStatus = True

	def run(self, frame):
		"""Run the tracker given a frame input."""
		if self.readyStatus == False:
			self.track(frame)
		else:
			time.sleep(0.001)

	def close(self):
		self.timerMatch.end()
		self.timerBrute.end()

	####### ------- track ------- #######
	# Takes a frame input and finds information about it.  The Frame is
	# input from the expresswayCam class having already been processed
	# (cropped, resized, etc.).
	def track(self, frame):
		"""Main function of Tracker class."""
		self.count = self.count + 1 # increment the counter
		
		if SV_DEMO:
			cv2.imshow('Base Frame' + self.loc, frame)
				
		# Run the FastFeatureDetector
		keypoints = self.fast.detect(frame, None)
		keypointsPreFilter = keypoints
		if SV_FILTER_KEYPOINTS:
			# Filter out all the points we dont want
			keypoints = self.keypointFilter(keypoints)
					
		# Get the descriptors for our keypoints
		keypointsFilt, descriptors = self.descFinder(keypoints, frame)

		# If the program has been running for long enough, start matching keypoints.
		# This gives us enough time to build up a nice background model for the keypoint
		# processor so that it isnt trying to brute force check 500 features.
		if self.count > SV_START_DELAY:
			# Pass keypoints to compute class
			current, average = self.computeSingle.run(keypointsFilt,descriptors)
			
			if SV_DEMO:	# Process the list of keypoints
				# Generate a blank frame
				blankFrame = frame.copy()

				# Draw keypoints and number of features that we're tracking
				output1 = cv2.drawKeypoints(blankFrame, keypointsPreFilter, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
				cv2.imshow('All Detected Features' + self.loc,output1)

				# Prepare the Pre-Post filtering comparison
				output2 = cv2.drawKeypoints(blankFrame, keypointsPreFilter, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
				output2 = cv2.drawKeypoints(output2, keypointsFilt, np.array([]), (255,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
				output2 = cv2.putText(output2,"Pre: {0:3.0f}".format(len(keypointsPreFilter)),(30,30), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0))
				output2 = cv2.putText(output2,"Post: {0:3.0f}".format(len(keypointsFilt)),(30,60), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0))
				cv2.imshow('Pre and Post Filtering of Features' + self.loc, output2)
				
				# Draw the matches between the two frames
				output3 = cv2.drawMatches(self.oldFrame, self.oldKeypoints, frame, keypointsFilt, goodMatches, None,
								flags = 2, singlePointColor = None, matchColor = (255, 0, 0))
				# Draw the current average speed onto the frame
				output3 = cv2.putText(out_img,"Speed: {0:06.2f} kph".format(self.averageSpeed),(30,30), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0,0,255))
				output3 = cv2.putText(out_img,"PPM: {0:06.2f}".format(_PPM),(30,60), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0,0,255))
				cv2.imshow('Matches and Speed Output' + self.loc,output3)

				# Draw static features
				cv2.imshow('Static Feature Ground-Truth' + self.loc, self.baseFrame)

				#for i in range(0,4):
				#	blankFrame = cv2.putText(blankFrame,"SP: {0:06.2f} kph".format(speedLane[i]),(30,30 + 30 * i), cv2.FONT_HERSHEY_DUPLEX, 0.4, (0,0,255))
				#cv2.imshow('Speed Output' + self.loc,blankFrame)

			# Update the constants dependent on traffic conditions
			# self.updateVariables()
								
		# We've finished the frames, so update everything
		self.oldFrame = frame.copy()
		self.oldDescripts = descriptors
		self.oldKeypoints = keypointsFilt
	

	####### ------- keypointFilter ------- #######
	# Processes the keypoints found by the FastFeatureDetector and looks
	# at these points to location static road features.  The function
	# builds a groundtruth image of static features and filters them from
	# cars and other vehicles features.
	def keypointFilter(self, keypoints):
		"""Processes the keypoints found by the FastFeatureDetector and looks for markings on the road."""
		# Make a blank list
		newKeypoints = []

		# Quickly update the entire frame based on the learning rate
		self.baseFrame = (self.baseFrame) * (1 - _LR1 / 3)

		# the keypoint check
		for i in range(0,len(keypoints)):
			# Pull coordinates from keypoint
			pointY = int(keypoints[i].pt[0])
			pointX = int(keypoints[i].pt[1])

			# Get the current value from the baseFrame at the given coordinates
			pointVal = self.baseFrame[pointX,pointY]

			# If there is no evidence of an existing point
			if pointVal <  0.5:
				# Append this keypoint to the list of good points
				newKeypoints.append(keypoints[i])
		
			# Update points around and including the keypoint
			self.baseFrame[pointX,pointY] = pointVal + 3 * _LR1
			self.baseFrame[pointX + 1,pointY] = pointVal + 1 * _LR1
			self.baseFrame[pointX - 1,pointY] = pointVal + 1 * _LR1
			self.baseFrame[pointX,pointY + 1] = pointVal + 1 * _LR1
			self.baseFrame[pointX,pointY - 1] = pointVal + 1 * _LR1
				
		return newKeypoints

	####### ------- keypointFilter ------- #######
	# Takes a keypoint and descriptor input, and segments them into groups
	# for each lane.
	def segmenter(self, key, dsc):
		"""Segments keypoints and descriptors into lane groups."""
		self.sortedKey = [[],[],[],[]]
		self.sortedDsc = [np.array([], dtype=np.uint8),np.array([], dtype=np.uint8),np.array([], dtype=np.uint8),np.array([], dtype=np.uint8)]
		for i in range(0,len(dsc)):
			y = key[i].pt[0]
			LANE = -1
			if y < self.height / 4:
				LANE = 0
			elif y >= self.height / 4 and y < self.height / 2:
				LANE = 1
			elif y >= self.height / 2 and y < (self.height / 4) * 3:
				LANE = 2
			else:
				LANE = 3
			self.sortedKey[LANE].append(key[i])
			if self.sortedDsc[LANE].size == 0:
				self.sortedDsc[LANE] = np.array(dsc[i], dtype=np.uint8)
			elif self.sortedDsc[LANE].ndim == 1:
				self.sortedDsc[LANE] = np.concatenate(([self.sortedDsc[LANE]],[dsc[i]]), axis = 0)
			else:
				self.sortedDsc[LANE] = np.concatenate((self.sortedDsc[LANE],[dsc[i]]), axis = 0)

		speedLane = []
		for i in range(0, self.LANES):
			current, average = self.compute[i].run(self.sortedKey[i],self.sortedDsc[i])
			speedLane.append(average)


	####### ------- descFinder ------- #######
	# Takes a list of keypoints and creates descriptors for them.  These
	# are created with BRIEF via ORB.
	def descFinder(self, kp, frame):
		"""Extracts descriptors for a given frame and set of keypoints.
		Takes an input of a vector of keypoints and a frame."""
		# Take inputs and extract descriptors
		kpo, dsc = self.descExtractor1.compute(frame, kp)

		# Return Keypoints and corresponding Descriptors
		return kpo, dsc

	####### ------- updateVariables ------- #######
	# Runs at the completion of each track() loop.  Updates lerarning rate
	# and other system variables for use in processing future frames.
	def updateVariables(self):
		"""Updates learning rates and other variables at the completion of each frame."""
		# Update the learning rate of the keypoint filter-er
		currSpeedFilt = self.averageSpeed
		if currSpeedFilt > _FILTER_SPEED:
			currSpeedFilt = _FILTER_SPEED
		_LR1 = _LR1_BASE * (_FILTER_SPEED / currSpeedFilt)


class trackerCompute:
	def __init__(self, LANES = 4, LANE = 1, LOC = "Top"):
		"""Handles the computation and comparison between descriptors in the tracker class."""
		self.LANES = LANES
		self.LANE = LANE

		self.oldDescripts = []
		self.oldKeypoints = []

		self.firstCount = True
		self.descBruteForce = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck = False)

		self.averageSpeed = 0			# weighted average speed of vehicles
		self.averageFrame = 9999		# weighted average pixel speed of vehicles
		self.currentSpeed = 0			# current speed of vehicles
		self.currentFrame = 9999		# current pixel speed of vehicles

		
		self.timerMatch = timer(ITERATIONS = 200, DISP_RPS = True, DISP_PERC = False, NAME = LOC + "-CLASS", ROOT = False, WRITE = False, DISP_TIME = True)


	def update(self, keypoints, descriptors):
		"""Update historic keypoints and descriptors to reflect input."""
		self.oldKeypoints = keypoints
		self.oldDescripts = descriptors

	def run(self, keypoints, descriptors):
		"""Run the compute class."""
		# Get matches and process them
		goodMatches = self.matchProcessor(self.descCompare(descriptors, type = "Standard"), keypoints)
		# Update class
		self.update(keypoints, descriptors)

		# Return relevant values
		return self.currentSpeed, self.averageSpeed

	def descCompare(self, dsc, type = "Standard"):
		"""Brute force checks for matches between two sets of descriptors.
		Takes an input of a vector of descriptors."""
		
		# Check to see there is actually something to compare
		if dsc is None or self.oldDescripts is None:
			return []
		elif (len(dsc) == 0 or len(self.oldDescripts) == 0):
			return []
		else:
			if dsc.ndim == 1:
				dsc = np.array([dsc])
			if self.oldDescripts.ndim == 1:
				self.oldDescripts = np.array([self.oldDescripts])
			# Matches points from input descriptors and the previous frames descriptors
			if type == "Standard":
				matchedPoints = self.descBruteForce.match(self.oldDescripts, dsc)
			elif type == "Radius":
				matchedPoints = self.descBruteForce.radiusMatch(self.oldDescripts, dsc, maxDistance = 10)
			else:
				matchedPoints = self.descFlannMatch.knnMatch(self.oldDescripts, dsc, k = 2)
			return matchedPoints
		
	####### ------- matchProcessor ------- #######
	# Takes matches from descCompare and processes them to find traffic
	# parameters.  Determines vehicle speeds and other parameters.
	def matchProcessor(self, matchedPoints, keypoints):
		"""Finds the distances between the different keypoints matched in the sequence.
		Takes inputs of matchedPoints then Keypoints."""

		# Make a blank list for values to be stored in
		distances = []
		goodMatches = []
		goodPoints = []
		goodDist = []
		currentDistances = []

		for i in range(0, len(matchedPoints)):
			if matchedPoints[i]:
				# Get the keypoint index
				a = matchedPoints[i].queryIdx	# index for "self.oldKeypoints"
				b = matchedPoints[i].trainIdx	# index for "keypoints

				# calculate the distance between the two sets of coordinates for the given index
				dist = math.sqrt(math.pow(int(self.oldKeypoints[a].pt[1]) - int(keypoints[b].pt[1]), 2)	+ math.pow(int(self.oldKeypoints[a].pt[0]) - int(keypoints[b].pt[0]), 2))
			
				# if the distance between the two points is reasonable, append it
				if dist < (self.averageFrame) * 2:
					currentDistances.append(dist)
					goodMatches.append(matchedPoints[i])

		# Look over the points for similar speeds
		if len(currentDistances) is not 0:
			# Make our blank array
			filteredDistances = []

			# Append the first cell to start things moving
			filteredDistances.append(currentDistances[0])

			# For the entire currentDistances array
			for i in range(1, len(currentDistances)):
				flag = 0	# set floating flag to zero
				
				# Iterate over all the current elements of the filtereDistances list.
				# If the current value matches any of them, dont include it.
				for j in range(0, len(filteredDistances)):
					if math.fabs(currentDistances[i] - filteredDistances[j]) < (currentDistances[i] * _PixDiff):
						flag += 1
				if flag is 0:
					filteredDistances.append(currentDistances[i])

			# Update the self.currentDistances list
			currentDistances = []
			currentDistances = filteredDistances

		# If we are running from live video
		if SV_RUN_LIVE:
			####### ------- PLEASE NOTE ------- #######
			# This needs to be corrected slightly to account for the different speeds at which frames are
			# being read when running in a live environment.  Not really sure how to approach the math for
			# this at the time of writing.  Going to need on-site time to get it configured correctly.

			# Get the current frames parameters
			self.currentFrame = (sum(currentDistances) / float(len(currentDistances))) * (1 / (self.timeFinish - self.timeStart))
			self.currentSpeed = (self.currentFrame / _PPM) * _MPS_to_KPH
			
			# If this is the first time running, set initial average parameters
			if self.firstCount:
				self.initSpeed()
				self.firstCount = False

			# Update the floating average values
			self.averageFrame = self.averageFrame * (1 - _LR2) + self.currentFrame * _LR2
			self.averageSpeed = self.averageSpeed * (1 - _LR2) + self.currentSpeed * _LR2
						
		# If we are running from a video file
		else:
			# Get the current frames parameters
			if len(currentDistances) is not 0:
				# There are cars in the frame, do analysis
				self.currentFrame = (float(sum(currentDistances)) / float(len(currentDistances)))
				self.currentSpeed = (self.currentFrame / float(_PPM)) * float(_MPS_to_KPH) / float(1 / _FPS)
			else: 
				# There are no cars in the frame, carry the averag speed from previous
				self.currentFrame = self.averageFrame
				self.currentSpeed = self.averageSpeed

			# If this is the first time running, set initial average parameters
			if self.firstCount:
				self.initSpeed()
				self.firstCount = False

			# Update the floating average values
			self.averageFrame = self.averageFrame * (1 - _LR2) + self.currentFrame * _LR2
			self.averageSpeed = self.averageSpeed * (1 - _LR2) + self.currentSpeed * _LR2

		return goodMatches


	####### ------- initSpeed ------- #######
	# Runs on the first use of class.  Sets the average speed of the system
	# to a non-zero number to allow processing to take place.
	def initSpeed(self):
		"""Runs on first use of the matchProcessor.  Sets the average speed of the system at tracking commencement."""
		# Set the average to the current to get the ball rolling
		self.averageFrame = self.currentFrame
		self.averageSpeed = self.currentSpeed