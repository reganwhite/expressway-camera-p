###### EXPRESSWAY CAMERA ######

# Declare the different libraries and what not that we might need
import numpy as np
import cv2
import time
import math
from adjuster import adjuster
from tracker import tracker
from adjuster import adjuster
import socket
from counter import counter
import sys
from threading import Thread
#import picamera
#import picamera.array

# Counter resolution
COUNT_RES = 2
SV_COUNT_UPDATE = 50
SV_TRACK = False
SV_COUNT = True
SV_LIVE	= False


###### ------- ewc ------- ######
# Settings class
class ewc:
	def __init__(cfg):
		#------------------------------------------------------------------------------------
		###### ------- GLOBAL settings ------- ######
		cfg.DEF_RES_W				= 1920
		cfg.DEF_RES_H				= 1080
		cfg.IM_BIN_SIZE				= 4

		cfg._X1						= 0
		cfg._X2						= 1360
		cfg._Y1						= 0
		cfg._Y2						= 1080
		cfg._W						= np.int(np.ceil((cfg._X2 - cfg._X1) / cfg.IM_BIN_SIZE))
		cfg._H						= np.int(np.ceil((cfg._Y2 - cfg._Y1) / cfg.IM_BIN_SIZE))

		#------------------------------------------------------------------------------------
		###### ------- expresswayCamera settings ------- ######
	
		cfg.SV_TRACK				= True
		cfg.SV_COUNT				= False
		cfg.SV_LIVE					= False
		cfg.COUNT_RES				= 3			# Counter resolution

		#------------------------------------------------------------------------------------
		###### ------- tracker settings ------- ######

		# Define some flags
		cfg.SV_USE_DEBUG			= True
		cfg.SV_FILTER_KEYPOINTS		= True
		cfg.SV_DEMO					= True		# FLAG FOR PROJECT DEMONSTRATION
		cfg.SV_RUN_LIVE				= False
		cfg.SV_SEND_DATA			= True

		####### ------- COMPONENT SETTINGS
		# Note that some of the settings may be deprecated and no longer in use.
		# They remain listed for posterity, as how the class functions is subject to
		# change.

		# Start Delay
		cfg.SV_START_DELAY			= 100		# number of frames the sytem will process before commencing analysis
		cfg.SV_SEND_DELAY			= 1000		# number of frames the system will process before sending to server

		# FAST (Fast Feature Detector)
		cfg.FFD_THRESHOLD			= 84
						# Can incremement this with fast.setThreshold

		# Descriptor Extractor
		cfg.ORB_NFEATURES			= 1
		cfg.ORB_SCALEFACTOR			= 1
		cfg.ORB_NLEVELS				= 1
		cfg.ORB_EDGETHRESH			= 3
		cfg.ORB_FIRSTLEVEL			= cfg.ORB_EDGETHRESH
		cfg.ORB_WTA_K				= 3
		cfg.ORB_SCORETYPE			= cv2.ORB_FAST_SCORE
		
		# Define other useful variables
		cfg._LR1					= 0.1		# Learning rate for keypoint remover
		cfg._LR1_BASE				= 0.1
		cfg._LR2					= 0.01		# Learning rate for Speed Updater
		cfg._LR2_BASE				= 0.01
		cfg._FPS					= float(30)	# FPS of video file if being read from a video
		cfg._PPM_UNSCALED			= 195
		cfg._PPM					= float( cfg._PPM_UNSCALED / cfg.IM_BIN_SIZE / 3)	# Number of Pixels-Per-Meter
		cfg._MPS_to_KPH				= float(3.6)	# constant
		cfg._PixDiff				= 0.05		# 
		cfg._FILTER_SPEED			= 30		# max concernable filter speed in kph

		#------------------------------------------------------------------------------------
		###### ------- adjuster settings ------- ######

		# Gaussian Blur
		cfg.GAUSS_KSIZE				= 0
		cfg.GAUSS_SIGMA_X			= 0
		cfg.GAUSS_SIGMA_Y			= 0

		#------------------------------------------------------------------------------------
		###### ------- counter settings ------- ######
		
		cfg.MAX_INT					= 255


class expresswayCamera:
	"""Main Class. Handles iteration over images."""

	def __init__(self):
		"""Initialize variables."""
		# Initialise the settings object inside a list
		self.cfg = [ewc()]

		# Get the system name to find the videofile
		name = socket.gethostname()

		# Initalize adjuster
		self.adj = adjuster()

		if self.cfg[0].SV_LIVE == False:
			# Figure out the location of the video file
			if name == "Regan-PC":
				CAP_VIDEOFILE = "E:/testVideoG.mp4"
			elif name == "Regan-Surface":
				CAP_VIDEOFILE = "C:/testVideoH.mp4"
			elif name == "RWHIT-PI801":
				CAP_VIDEOFILE = "testVideoH.mp4"
			else:
				sys.exit("Dont know what device this is running on. Exitting.")

			# Initiate our Frame Capture
			self.frameCapture = cv2.VideoCapture(CAP_VIDEOFILE)

			# Get frames for initialising background models
			success, frame = self.frameCapture.read()
			top, bot = self.adj.adjust(frame)
		else:
			self.grabber = frameGrabber()
			self.grabber.start()
			top, bot = self.adj.adjust(frame, resize = False)

		if self.cfg[0].SV_TRACK:
			# Initialize the objects
			self.top_track = tracker("Top",top)
			self.bot_track = tracker("Bot",bot)

		if self.cfg[0].SV_COUNT:
			# Initialize the counters.
			self.top_count = counter(top, "Top", right = self.cfg[0].COUNT_RES, left = self.cfg[0].COUNT_RES, lr = 0.02)
			self.bot_count = counter(bot, "Bot", right = self.cfg[0].COUNT_RES, left = self.cfg[0].COUNT_RES, lr = 0.02)

		self.frame_time = time.time()

	def loop(self):
		"""Main loop of expresswayCam class"""
		# While there are still frames to be read
		count = 0
		float = 0
		while self.frameCapture.isOpened():
			count = count + 1
			# get the next frame
			if count % 100 == 1:
				time1 = time.time()
			success, frame = self.frameCapture.read()
			if success:
				self.frame_time = time.time()
				top, bot = self.adj.adjust(frame)
				
				if self.cfg[0].SV_TRACK:
					self.top_track.track(top)
					self.bot_track.track(bot)

				if self.cfg[0].SV_COUNT:
					self.top_count.run(top)
					self.bot_count.run(bot)
			else:
				print("Looks like we've run out of frames to read.")
				print("This is either because of an error, or because we've finished reading the file.")
				quit()

			# Wait for key input and exit on Q
			key = cv2.waitKey(1) & 0xff
			if key == ord('q'):
				break

			if count % 100 == 0 and count > 100:
				print('\r[FPS] = {0:2.3f}'.format(100/(time.time() - time1)))

		# Release the frame capture and exit the function
		self.frameCapture.release()

		# Release the frame capture and exit the function
		self.count_runStatus = False
		self.track_runStatus = False
		self.frameCapture.release()

	def countRoutineHandle(self):
		"""Threaded routine for counters."""
		while(self.count_runStatus):
			if (self.count_readyStatus):
				self.top_count.run(self.frame_ready[0], self.frame_ready[1])

	def countRoutineStart(self):
		"""Start the thread for the counting routine."""
		Thread(target = self.countRoutineHandle, args = ()).start()

#class frameGrabber:
#	"""Grabs frames from the piCamera."""
	
#	def __init__(self, sensor_mode = 6, resolution = '128x72', framerate = 30):
#		"""Initialize variables."""
#		# Settings initialised thanks to StackExchange post by Dave Jones on 14th December, 2016
#		# Accessed 25/07/17
#		# https://raspberrypi.stackexchange.com/questions/58871/pi-camera-v2-fast-full-sensor-capture-mode-with-downsampling

#		# PiCamera object
#		self.cam = picamera()

#		# -----------------------------------------------------------------------------------
#		# Pi Camera v2 Sensor Modes - https://i.stack.imgur.com/rHObK.jpg
#		# -----------------------------------------------------------------------------------
#		#	Mode	Resolution		A/R		FPS			Video	Image	FoV			Binning
#		#	1		1920x1080		16:9	0.1-30fps	x	 			Partial		None
#		#	2		3280x2464		4:3		0.1-15fps	x		x		Full		None
#		#	3		3280x2464		4:3		0.1-15fps	x		x		Full		None
#		#	4		1640x1232		4:3		0.1-40fps	x	 			Full		2x2
#		#	5		1640x922		16:9	0.1-40fps	x	 			Full		2x2
#		#	6		1280x720		16:9	40-90fps	x	 			Partial		2x2
#		#	7		640x480			4:3		40-90fps	x	 			Partial		2x2
#		# -----------------------------------------------------------------------------------
#		self.cam.sensor_mode = sensor_mode

#		# Other Settings
#		self.cam.resolution = resolution	# Resolution for the Pi's GPU needs to downsample frame to
#		self.cam.framerate = framerate			# Target framerate for the Raspberry Pi to aim for.

#		# Make our blank frame for storage
#		self.frame_latest	= np.empty((72, 128), dtype = np.uint8)
#		# Set up a variable for us to store the time at which the frame is pulled
#		self.frame_time		= time.time()
		
#		# Initialize counter
#		self.count = 0

#	def update(self):
#		"""Updater for the settings which determine the Pi Camera's Operation."""
#		# This it the groundwork for the function which will determine the operation of the Rasberry Pi camera in a number of
#		# different environments.  For example, as the lighting conditions in the scene change so will settings such as shutter
#		# speed and white balance, and this function will handle the configuring of those settings to ensure optimum opeartion
#		# of the system.
#		foo = 1

#	def start(self):
#		"""Start the thread for the counting routine."""
#		Thread(target = self.run, args = ()).start()
#		return 1

#	def run(self):
#		"""Main loop of the frameGrabber class."""
#		# Go to sleep to give the camera some time to warm up
#		time.sleep(1)

#		# Enter the while loop
#		while True:
#			self.count += 1

#			if self.count % SV_CAM_UPDATE == 0:
#				# Update the camera to make sure it's still running properly
#				self.update()

#			# Start the frame pull
#			try:
#				self.cam.capture(new,'bgr')		# Pull the frame from the camera
#			except:
#				print("Looks like something went horribly wrong with the Frame Read.")
#				print("Complain to Regan and get him to fix this.")

#			self.frame_time = time.time()	# Record the frame time	
#			self.frame_latest = new.copy()	# copy it to the self.frame_latest variable
		
#		print "Exitting frameGrabber."

#	def time(self, t):
#		"""Compares the previous frame time to the current frame time."""
#		# Compare the times.
#		if t == self.frame_time:
#			return 2
#		elif t > self.frame_time:
#			return 3
#		else:
#			return 1

#	def grab(self):
#		"""Grabs the latest frame."""
#		# Return the latest frame.
#		return self.frame_latest
		


if __name__ == '__main__':
	# Initialize the tracker object
	main = expresswayCamera()
	main.loop()

	# Make sure everything is cleaned up
	cv2.destroyAllWindows()