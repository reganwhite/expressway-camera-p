# Declare the different libraries and what not that we might need
import numpy as np
import cv2
import time
import math
from ewctools import requester
import string
import random
from ewctools import timer

####### ------- EXPRESSWAY TRACKER MK.2 ------- #######
class tracker:
	"""Class used to track vehicles."""

	def __init__(self, frameInit, settings, loc):
		"""Initialize things."""

		# import settings
		self.cfg = settings

		if loc == "Top":
			self.cfg._PPM_UNSCALED = float(178)
		else:
			self.cfg._PPM_UNSCALED = float(205)

		self.cfg._PPM = float( self.cfg._PPM_UNSCALED / self.cfg.IM_BIN_SIZE / 3)

		self.requester = requester('http://regandwhite.com/traffic/data/entry.php', loc)
		self.loc = " " + loc

		# Make the fast corner detector
		self.fast = cv2.FastFeatureDetector_create(self.cfg.FFD_THRESHOLD)

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
		self.descExtractor1 = cv2.ORB_create(edgeThreshold = self.cfg.ORB_EDGETHRESH, patchSize = self.cfg.ORB_EDGETHRESH,
											WTA_K = self.cfg.ORB_WTA_K, scoreType = self.cfg.ORB_SCORETYPE)

		# Point Matcher
		self.descBruteForce = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck = False)
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
			self.compute.append(trackerCompute(self.cfg, LANES = 4, LANE = i))
		self.computeSingle = trackerCompute(self.cfg, LANES = 1, LANE = 1, LOC = loc)


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

		self.readyStatus = True
		
	def close(self):
		self.timerMatch.end()
		self.timerBrute.end()

	def reset(self):
		"""Reset all tracking variables such that a new set of frames can be analysed."""
		self.computeSingle.reset()	# reset the single compute object

		for i in range(0,self.LANES):
			self.compute[i].reset()	# reset the multi-lane compute object

	def send(self):
		"""Send the cyrrent average speed from the compute module to the web server."""
		# build multilane string
		if self.cfg.SV_MULTILANE:
				multi = str(self.compute[0].retSpeed()) + "|" + str(self.compute[1].retSpeed()) + "|" + str(self.compute[2].retSpeed()) + "|" + str(self.compute[3].retSpeed())
		else:
			multi = "0|0|0|0"

		self.requester.startSendSpeed(self.computeSingle.retSpeed(), time.time() + 36000, multi, self.loc)

	####### ------- track ------- #######
	# Takes a frame input and finds information about it.  The Frame is
	# input from the expresswayCam class having already been processed
	# (cropped, resized, etc.).
	def track(self, frame, frametime = False):
		"""Main function of Tracker class."""
		self.count = self.count + 1 # increment the counter
		
		if self.cfg.SV_DEMO:
			cv2.imshow('Base Frame' + self.loc, frame)
				
		# Run the FastFeatureDetector
		keypoints = self.fast.detect(frame, None)
		keypointsPreFilter = keypoints
		if self.cfg.SV_FILTER_KEYPOINTS:
			# Filter out all the points we dont want
			keypoints = self.keypointFilter(keypoints)
					
		# Get the descriptors for our keypoints
		keypointsFilt, descriptors = self.descFinder(keypoints, frame)

		# If the program has been running for long enough, start matching keypoints.
		# This gives us enough time to build up a nice background model for the keypoint
		# processor so that it isnt trying to brute force check 500 features.
		if self.count > self.cfg.SV_START_DELAY:
			# Pass keypoints to compute class
			if self.cfg.SV_MULTILANE:
				average = self.segmenter(keypointsFilt, descriptors, frametime)
				current, average = self.computeSingle.run(keypointsFilt,descriptors, frametime)
			else:
				current, average = self.computeSingle.run(keypointsFilt,descriptors, frametime)
			
			if self.cfg.SV_DEMO:	# Process the list of keypoints
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
				output3 = cv2.drawMatches(self.oldFrame, self.oldKeypoints, frame, keypointsFilt, self.computeSingle.goodMatches, None,
								flags = 2, singlePointColor = None, matchColor = (255, 0, 0))
				# Draw the current average speed onto the frame
				output3 = cv2.putText(output3,"Speed: {0:06.2f} kph".format(self.computeSingle.averageSpeed),(30,30), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0,0,255))
				output3 = cv2.putText(output3,"PPM: {0:06.2f}".format(self.cfg._PPM),(30,60), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0,0,255))
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
		self.baseFrame = (self.baseFrame) * (1 - self.cfg._LR1 / 3)

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
			self.baseFrame[pointX,pointY] = pointVal + 3 * self.cfg._LR1
			self.baseFrame[pointX + 1,pointY] = pointVal + 1 * self.cfg._LR1
			self.baseFrame[pointX - 1,pointY] = pointVal + 1 * self.cfg._LR1
			self.baseFrame[pointX,pointY + 1] = pointVal + 1 * self.cfg._LR1
			self.baseFrame[pointX,pointY - 1] = pointVal + 1 * self.cfg._LR1
				
		return newKeypoints

	####### ------- segmenter ------- #######
	# Takes a keypoint and descriptor input, and segments them into groups
	# for each lane.
	def segmenter(self, key, dsc, frametime):
		"""Segments keypoints and descriptors into lane groups."""
		self.sortedKey = [[],[],[],[]]	# make blank list of lists for sorted keypoints
		self.sortedDsc = [np.array([], dtype=np.uint8),np.array([], dtype=np.uint8),np.array([], dtype=np.uint8),np.array([], dtype=np.uint8)]	# make blank list of numpy arrays for sorted descriptors
		
		speedLane = []
			
		# for all keypoints and descriptors
		if dsc is not None:
			for i in range(0,len(dsc)):
				y = key[i].pt[0]	# get y coordinate of keypoint
				LANE = -1
				# determine lane by the height of the keypoint
				if y < self.height / 4:
					LANE = 0
				elif y >= self.height / 4 and y < self.height / 2:
					LANE = 1
				elif y >= self.height / 2 and y < (self.height / 4) * 3:
					LANE = 2
				else:
					LANE = 3
				# append keypoint to desired lane
				self.sortedKey[LANE].append(key[i])

				# append descriptor to desired lane
				if self.sortedDsc[LANE].size == 0:
				# if emtpy, initialize the lane with a numpy array containing the descriptor
					self.sortedDsc[LANE] = np.array(dsc[i], dtype=np.uint8)
				elif self.sortedDsc[LANE].ndim == 1:
				# if a single descriptor already exists, concatenate as list
					self.sortedDsc[LANE] = np.concatenate(([self.sortedDsc[LANE]],[dsc[i]]), axis = 0)
				else:
					self.sortedDsc[LANE] = np.concatenate((self.sortedDsc[LANE],[dsc[i]]), axis = 0)

			for i in range(0, self.LANES):
				current, average = self.compute[i].run(self.sortedKey[i],self.sortedDsc[i], frametime)
				speedLane.append(average)

		return speedLane


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
		if currSpeedFilt > self.cfg._FILTER_SPEED:
			currSpeedFilt = self.cfg._FILTER_SPEED
		self.cfg._LR1 = self.cfg._LR1_BASE * (self.cfg._FILTER_SPEED / currSpeedFilt)

####### ------- EXPRESSWAY TRACKER COMPUTE MODULE ------- #######
class trackerCompute:
	def __init__(self, settings, LANES = 4, LANE = 1, LOC = "Top"):
		"""Handles the computation and comparison between descriptors in the tracker class."""
		self.cfg = settings # import settings
		
		self.LANES = LANES	# How many lanes are there?
		self.LANE = LANE	# Which lane is this module?

		self.LOC = LOC	# is this the top or the bottom?
		
		self.firstCount = True	# Do we need to initialise values on this run?
		
		self.oldKeypoints = []	# historical keypoints
		self.oldDescripts = []	# historical descriptors

		self.previousAverageSpeed = 0	# weighted average speed of vehicles
		self.previousAverageFrame = 0	# weighted average pixel speed of vehicles

		self.averageSpeed = 0		# weighted average speed of vehicles
		self.averageFrame = 9999	# weighted average pixel speed of vehicles
		self.currentSpeed = 0		# current speed of vehicles
		self.currentFrame = 9999	# current pixel speed of vehicles

		self.lastFrameTime = 0	# when did we read the last frame?
		
		self.descBruteForce = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck = True)	# initialize matcher

		# initialize match mask variables
		self.MASK = np.array(0, dtype=np.uint16)
		self.xO = np.array(0, dtype=np.uint16)
		self.yO = np.array(0, dtype=np.uint16)

		self.timerMatch = timer(ITERATIONS = 200, DISP_RPS = True, DISP_PERC = False, NAME = LOC + "-CLASS", ROOT = False, WRITE = False, DISP_TIME = True)

	def reset(self):
		"""Reset all tracking variables in the compute module such that a new set of frames can be analysed."""
		self.firstCount = True	# Do we need to initialise values on this run?
		
		self.oldKeypoints = []	# historical keypoints
		self.oldDescripts = []	# historical descriptors

		self.previousAverageSpeed = self.averageSpeed	# weighted average speed of vehicles
		self.previousAverageFrame = self.averageFrame	# weighted average pixel speed of vehicles

		self.averageSpeed = 0		# weighted average speed of vehicles
		self.averageFrame = 9999	# weighted average pixel speed of vehicles
		self.currentSpeed = 0		# current speed of vehicles
		self.currentFrame = 9999	# current pixel speed of vehicles

		self.goodMatches = []


	def retSpeed(self):
		"""Returns the average speed of the object"""
		return self.averageSpeed # / (self.cfg.TR_BUFFER_SIZE - 1)

	def update(self, keypoints, descriptors, frametime = False):
		"""Update historic keypoints and descriptors to reflect input."""
		self.oldKeypoints = keypoints
		self.oldDescripts = descriptors

		if frametime:
			self.lastFrameTime = frametime

	def masker(self, keypoints):
		"""Finds the mask of appropriate keypoints."""
		self.MASK = np.zeros((20,15), dtype=np.uint16)

		return mask

	def run(self, keypoints, descriptors, frametime):
		"""Run the compute class."""
		# Get matches and process them
		self.goodMatches = self.matchProcessor(self.descCompare(descriptors, type = "Standard"), keypoints, frametime)
		# Update class
		self.update(keypoints, descriptors, frametime)

		# Return relevant values
		return self.currentSpeed, self.averageSpeed

	def descCompare(self, dsc, type = "Standard"):
		"""Brute force checks for matches between two sets of descriptors. Takes an input of a list of descriptors."""
		
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

			# Match points from input descriptors and the historic descriptors
			if type == "Standard":
			# standard matcher
				matchedPoints = self.descBruteForce.match(self.oldDescripts, dsc)
			elif type == "Radius":
			# standard matcher with radius filtering
				matchedPoints = self.descBruteForce.radiusMatch(self.oldDescripts, dsc, maxDistance = 10)
			else:
			# flann matcher with knn matching
				matchedPoints = self.descFlannMatch.knnMatch(self.oldDescripts, dsc, k = 2)

			return matchedPoints
		
	####### ------- matchProcessor ------- #######
	# Takes matches from descCompare and processes them to find traffic
	# parameters.  Determines vehicle speeds and other parameters.
	def matchProcessor(self, matchedPoints, keypoints, frametime = False):
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

				yDiff = int(self.oldKeypoints[a].pt[1]) - int(keypoints[b].pt[1])
				xDiff = int(self.oldKeypoints[a].pt[0]) - int(keypoints[b].pt[0])

				# calculate the distance between the two sets of coordinates for the given index
				dist = math.sqrt(math.pow(yDiff, 2)	+ math.pow(xDiff, 2))
			
				if np.abs(yDiff) <= 5:
					# if the distance between the two points is reasonable, append it
					if dist < (30):	# and dist < (20 * 2)  ---- CAUSES ISSUES IN LIVE OPERATION ---- dist < (self.previousAverageFrame) * 1.5 and
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
					if math.fabs(currentDistances[i] - filteredDistances[j]) < (currentDistances[i] * self.cfg._PixDiff):
						flag += 1
				if flag is 0:
					filteredDistances.append(currentDistances[i])

			# Update the self.currentDistances list
			currentDistances = []
			currentDistances = filteredDistances

		# If we are running from live video
		if frametime:
			# Get the current frames parameters
			if len(currentDistances) is not 0:
				tDiff = frametime - self.lastFrameTime # Time difference
				if self.lastFrameTime == 0:
					tDiff = float(1 / self.cfg._FPS)
				# There are cars in the frame, do analysis
				self.currentFrame = (float(sum(currentDistances)) / float(len(currentDistances)))
				self.currentSpeed = (self.currentFrame / float(self.cfg._PPM)) * float(self.cfg._MPS_to_KPH) / float(tDiff)
				# If this is the first time running, set initial average parameters
				if self.firstCount:
					self.initSpeed(frametime)
			else:
				# There are no cars in the frame, carry the averagee speed from previous
				self.currentFrame = self.averageFrame
				self.currentSpeed = self.averageSpeed
			
		# If we are running from a video file
		else:
			# Get the current frames parameters
			if len(currentDistances) is not 0:
				# There are cars in the frame, do analysis
				self.currentFrame = (float(sum(currentDistances)) / float(len(currentDistances)))
				self.currentSpeed = (self.currentFrame / float(self.cfg._PPM)) * float(self.cfg._MPS_to_KPH) / float(1 / self.cfg._FPS)
				# If this is the first time running, set initial average parameters
				if self.firstCount:
					self.initSpeed()
			else:
				# There are no cars in the frame, carry the average speed from previous
				self.currentFrame = self.averageFrame
				self.currentSpeed = self.averageSpeed
			
		# Update the floating average values
		self.averageFrame = self.averageFrame * (1 - self.cfg._LR2) + self.currentFrame * self.cfg._LR2
		self.averageSpeed = self.averageSpeed * (1 - self.cfg._LR2) + self.currentSpeed * self.cfg._LR2

		return goodMatches


	####### ------- initSpeed ------- #######
	# Runs on the first use of class.  Sets the average speed of the system
	# to a non-zero number to allow processing to take place.
	def initSpeed(self):
		"""Runs on first use of the matchProcessor.  Sets the average speed of the system at tracking commencement."""
		# Set the average to the current to get the ball rolling
		self.averageFrame = self.previousAverageFrame * (1 - self.cfg._LR2) + self.currentFrame * self.cfg._LR2
		self.averageSpeed = self.previousAverageSpeed * (1 - self.cfg._LR2) + self.currentSpeed * self.cfg._LR2

		self.firstCount = False