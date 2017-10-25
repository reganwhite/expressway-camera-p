###### EXPRESSWAY CAMERA ######
# Written and built for use with Python 2.7.9 and OpenCV 3.3.0
#

# Declare the different libraries and what not that we might need
import numpy as np
import cv2
if cv2.__version__ < "3.2.0":
	print("The ExpresswayCamera software was designed using OpenCV version 3.3.0.\n")
	print("This system is running with OpenCV  " + cv2.__version__ + ", which might not be supported.\n")
	print("Be aware that if your OpenCV is not at least version 3.2.0, the system")
	print("may be unstable, or not function correctly.")

import time
import socket
import sys
import traceback
from tracker import tracker
from counter import counter
from threading import Thread
from ewctools import timer, adjuster
import picamera
import picamera.array

###### ------- ewc ------- ######
# Settings class
class ewc:
	def __init__(cfg):
		#------------------------------------------------------------------------------------
		###### ------- expresswayCamera settings ------- ######
	
		cfg.SV_USE_DEBUG			= False
		cfg.SV_DEMO					= False
		cfg.SV_TRACK				= True
		cfg.SV_COUNT				= False
		cfg.SV_LIVE					= True

		#------------------------------------------------------------------------------------
		###### ------- GLOBAL settings ------- ######
		cfg.DEF_RES_W				= 1920
		cfg.DEF_RES_H				= 1080

		cfg._X1						= 0
		cfg._X2						= 1360
		cfg._Y1						= 0
		cfg._Y2						= 1080
		
		#------------------------------------------------------------------------------------
		###### ------- counter settings ------- ######
		cfg.COUNT_RES				= 4  		# Counter resolution
		cfg.MAX_INT					= 255

		#------------------------------------------------------------------------------------
		###### ------- tracker settings ------- ######

		# Define some flags
		cfg.SV_FILTER_KEYPOINTS		= True
		cfg.SV_RUN_LIVE				= False
		cfg.SV_SEND_DATA			= True
		cfg.TR_BUFFER_SIZE			= 6			# number of frames
		cfg.SV_SLEEP_DURATION		= 0.1		# seconds
		cfg.SV_MULTILANE			= False		# do multilane calculations?

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
		cfg._LR2					= 0.05		# Learning rate for Speed Updater
		cfg._LR2_BASE				= 0.05
		cfg._FPS					= float(30)	# FPS of video file if being read from a video
		cfg._FG_CAMERA_MODE			= 7
		cfg._FG_WIDTH				= 640
		cfg._FG_HEIGHT				= 480
		cfg._FG_RESOLUTION			= str(cfg._FG_WIDTH) + "x" + str(cfg._FG_HEIGHT)
		cfg._FG_FRAMERATE			= 30
		cfg._PPM_UNSCALED			= 195

		# Downsample Size
		cfg.IM_BIN_SIZE				= cfg.DEF_RES_H / cfg._FG_HEIGHT

		cfg._PPM					= float(cfg._PPM_UNSCALED / cfg.IM_BIN_SIZE / 3)	# Number of Pixels-Per-Meter
		cfg._MPS_to_KPH				= float(3.6)	# constant
		cfg._PixDiff				= 0.05		#
		cfg._FILTER_SPEED			= 30		# max concernable filter speed in kph


		cfg._W						= np.int(np.ceil((cfg._X2 - cfg._X1) / cfg.IM_BIN_SIZE))
		cfg._H						= np.int(np.ceil((cfg._Y2 - cfg._Y1) / cfg.IM_BIN_SIZE))

		#------------------------------------------------------------------------------------
		###### ------- adjuster settings ------- ######
		# Gaussian Blur
		cfg.GAUSS_KSIZE				= 0
		cfg.GAUSS_SIGMA_X			= 0
		cfg.GAUSS_SIGMA_Y			= 0
		

###### ------- expresswayCamera ------- ######
# Main Project Class
class expresswayCamera:
	"""Main Class. Handles iteration over images."""

	def __init__(self):
		"""Initialize variables."""
		# Initialise the settings object inside a list
		print("---------------------------------------------------------------------------")
		print("---------------------------- Expressway Camera ----------------------------\n")
		print("A Computer Vision Project by Regan White.")
		print("Made using Python 2.7.9+ and OpenCV 3.3.0.")
		print("Built and tested for the Raspberry Pi 3.")
		print("Designed for use on the Riverside Expressway in Brisbane, Australia.\n")
		print("---------------------------------------------------------------------------")
		print("Initializing...")
		try:
			print("Importing Settings...")
			self.cfg = ewc()
		except Exception as e:
			traceback.print_exc()
			quit("Settings Import failed. Closing.")
			
		# Initalize adjuster
		self.adj = adjuster(self.cfg)
		
		if self.cfg.SV_LIVE == False:
			print("Getting host name...")
			name = socket.gethostname()

			# Figure out the location of the video file
			if name == "Regan-PC":
				CAP_VIDEOFILE = "E:/testVideoH.mp4"
			elif name == "Regan-Surface":
				CAP_VIDEOFILE = "C:/testVideoH.mp4"
			elif name == "RWHIT-PI801":
				CAP_VIDEOFILE = "testVideoH.mp4"
			else:
				quit("Don't know what device this is running on. Closing.")

			# Initiate our Frame Capture
			try:
				print("Starting video capture from file...")
				self.frameCapture = cv2.VideoCapture(CAP_VIDEOFILE)
			except Exception as e:
				traceback.print_exc()
				quit("Video capture failed. Closing.")

			# Get frames for initialising background models
			success, frame = self.frameCapture.read()
			inbound, outbound = self.adj.adjust(frame)
		else:
			try:
				print("Initializing PiCamera capture.")
				self.grabber = frameGrabber(sensor_mode = self.cfg._FG_CAMERA_MODE, resolution = self.cfg._FG_RESOLUTION,
								framerate = self.cfg._FG_FRAMERATE, bufferSize = self.cfg.TR_BUFFER_SIZE)	# initialize the frame grabber object
			except Exception as e:
				traceback.print_exc()
				quit("PiCamera initializing failed.")
			
			try:
				frame = self.grabber.getSingle()	# get a single frame from the frame grabber for initialization
				inbound, outbound = self.adj.adjust(frame, resize = False, fromFile = False, crop = False)	# separate our frame into inbound and outbound
			except Exception as e:
				traceback.print_exc()
				quit("Failed to separate input frame into inbound/outbound.")

		if self.cfg.SV_TRACK:
		# Initialize the trackers objects
			self.inboundTrack = tracker(inbound, self.cfg, "Top")	# inbound
			self.outboundTrack = tracker(outbound, self.cfg, "Bot")	# outbound

		if self.cfg.SV_COUNT:
		# Initialize the counters objects
			self.inboundCount = counter(inbound, self.cfg, "Top", right = self.cfg.COUNT_RES, left = self.cfg.COUNT_RES, LR = 0.02) # inbound
			self.outboundCount = counter(outbound, self.cfg, "Bot", right = self.cfg.COUNT_RES, left = self.cfg.COUNT_RES, LR = 0.02) # outbound

		# Initialize the counters objects
		self.timer_root	 = timer(USE = self.cfg.SV_USE_DEBUG, NAME = "FPS", ROOT = True)
		self.timer_count = timer(USE = self.cfg.SV_USE_DEBUG, NAME = "CPS", DISP_TIME = False, DISP_PERC = True)
		self.timer_track = timer(USE = self.cfg.SV_USE_DEBUG, NAME = "TPS", DISP_TIME = False)
		self.timer_read	 = timer(USE = self.cfg.SV_USE_DEBUG, NAME = "RPS", DISP_TIME = False, DISP_PERC = True)

	def loop(self):
		"""Main loop of expresswayCam class"""
		# While there are still frames to be read
		count = 0
		while self.frameCapture.isOpened():
			count = count + 1

			self.timer_root.tik()
			self.timer_read.tik()

			# Read frame from file
			success, frame = self.frameCapture.read()

			self.timer_read.tok()

			if success:
				inbound, outbound = self.adj.adjust(frame)
				
				if self.cfg.SV_TRACK:
					self.timer_track.tik()

					self.inboundTrack.track(inbound)
					self.outboundTrack.track(outbound)

					self.timer_track.tok()

				if self.cfg.SV_COUNT:
					self.timer_count.tik()

					tc = self.inboundCount.run(inbound)
					bc = self.outboundCount.run(outbound)

					if count % 100 == 0 and count > 100:
						print("----------")
						print(tc)
						print(bc)
						print("----------")

					self.timer_count.tok()
			else:
				self.inboundTrack.close()
				self.outboundTrack.close()
				print("Looks like we've run out of frames to read.")
				print("This is either because of an error, or because we've finished reading the file.")
				print("Total frame count: {0:}".format(count))
				quit()

			# Wait for key input and exit on Q
			key = cv2.waitKey(1) & 0xff
			if key == ord('q'):
				break
			
			self.timer_root.tok()

		# Release the frame capture and exit the function
		self.frameCapture.release()

	def loopLiveTest(self):
		"""Main loop of expresswayCam class"""

		count = 0

		while 1:
			count = count + 1
			
			success, timeBuffer, frameBuffer = self.grabber.getBuffer()

			if success:
				# Quickly reset the instances back to default settings
				self.inboundTrack.reset()
				self.outboundTrack.reset()

				# For all of the variables in the buffer
				for i in range(0, self.cfg.TR_BUFFER_SIZE):
					try:
						inbound, outbound = self.adj.adjust(frameBuffer[i], crop = False, resize = False, cvt = True, fromFile = False) # read frame from buffer and process
					except Exception as e:
						traceback.print_exc()
					else:
						# Start frame processing
						if self.cfg.SV_TRACK:
						# If tracking is enabled
							try:
								self.inboundTrack.track(inbound, timeBuffer[i]) # inbound tracker
							except Exception as e:
								traceback.print_exc()
								print("Tracking of inbound lane failed. Continuing.")

							try:
								self.outboundTrack.track(outbound, timeBuffer[i]) # outbound tracker
							except Exception as e:
								traceback.print_exc()
								print("Tracking of outbound lane failed. Continuing.")

						if self.cfg.SV_COUNT:
						# If counting is enabled
							self.inboundCount.count(inbound)
							self.outboundCount.count(inbound)

				self.inboundTrack.send()
				self.outboundTrack.send()
						
			else:
				print("Looks like we haven't got any frames to read.")
				print("This is either because of an error, or because we've finished reading the file.")
				print("Total loops completed: {0:}".format(count))
				quit()

			# Wait for key input and exit on Q
			key = cv2.waitKey(1) & 0xff
			if key == ord('q'):
				break

			# Go to sleep for and wait for the next value to be read
			time.sleep(self.cfg.SV_SLEEP_DURATION)
	
###### ------- frameGrabber ------- ######
# Frame collection and processing class for use in live application.
class frameGrabber:
	"""Grabs frames from the piCamera."""
	
	def __init__(self, sensor_mode = 7, resolution = '640x480', framerate = 30, bufferSize = 6):
		"""Initialize variables."""
		# PiCamera object
		self.cam = picamera.PiCamera()

		# -----------------------------------------------------------------------------------
		# Pi Camera v2 Sensor Modes - http://traffic.regandwhite.com/include/images/PiCamera-modes.jpg
		# -----------------------------------------------------------------------------------
		#	Mode	Resolution		A/R		FPS			Video	Image	FoV			Binning
		#	1		1920x1080		16:9	0.1-30fps	x				Partial		None
		#	2		3280x2464		4:3		0.1-15fps	x		x		Full		None
		#	3		3280x2464		4:3		0.1-15fps	x		x		Full		None
		#	4		1640x1232		4:3		0.1-40fps	x				Full		2x2
		#	5		1640x922		16:9	0.1-40fps	x				Full		2x2
		#	6		1280x720		16:9	40-90fps	x				Partial		2x2		<----------------
		#	7		640x480			4:3		40-90fps	x				Partial		2x2		<----------------
		# -----------------------------------------------------------------------------------
		#
		# We're going to use mode 7
		self.cam.sensor_mode = sensor_mode

		# Other Settings
		self.cam.resolution = resolution # Resolution for the Pi's GPU needs to downsample frame to
		self.cam.framerate = framerate	# Target framerate for the Raspberry Pi to aim for.
				
		self.count = 0 # Initialize counter

		self.bufferSize = bufferSize # How big is the tracking modules buffer?
		self.frameBuffer = []
		self.timeBuffer = []

		self.stream = picamera.array.PiRGBArray(self.cam)	# initialise stream object for easy frame capture into numpy array

	def update(self):
		"""Updater for the settings which determine the Pi Camera's Operation."""
		# This it the groundwork for the function which will determine the operation of the Rasberry Pi camera in a number of
		# different environments.  For example, as the lighting conditions in the scene change so will settings such as shutter
		# speed and white balance, and this function will handle the configuring of those settings to ensure optimum opeartion
		# of the system.
		foo = 1
		
	def getSingle(self):
		"""Get a single frame for init."""
		self.stream.truncate(0)				# reset the stream as a precautionary measure
		self.cam.capture(self.stream,'bgr')	# use the pi camera object to capture a frame to stream in BGR colourspace
		return self.stream.array			# return the frame array

	def getBuffer(self):
		"""Runs a single instance of the capture loop"""
		# Reset buffers
		self.frameBuffer = []
		self.timeBuffer = []
		
		self.stream.truncate(0) # reset the stream as a precautionary measure

		try:
		# Build the buffer
			for i in range(0, self.bufferSize):
				self.timeBuffer.append(time.time())			# take the capture time and append it to the time buffer
				self.cam.capture(self.stream,'bgr')			# use the pi camera object to capture a frame to stream in BGR colourspace
				self.frameBuffer.append(self.stream.array)	# pull the frame from the camera and append it to the frame buffer
				self.stream.truncate(0)						# reset the stream
		except Exception as e:
		# Building the buffer has failed
			traceback.print_exc()
			print("Error getting frame buffer.")
			return False, self.timeBuffer, self.frameBuffer
		else:
		# Building the buffer was successful
			return True, self.timeBuffer, self.frameBuffer	# return the time and frame buffers


def operationModeInit(cfg):
	"""Configure the operation mode of the Expressway Camera system."""
	# Configure some of the operation modes
	if getInputFlag("Show mode select settings ('No' will set modes to default operation)?"):
		cfg.SV_RUN_LIVE = getInputFlag("Operate in Live Mode?")
		cfg.SV_DEMO = getInputFlag("Operate in Demo Mode?")
		cfg.SV_FILTER_KEYPOINTS = getInputFlag("Use keypoint filtering?")
		cfg.SV_USE_DEBUG = getInputFlag("Run in debug mode?")
		cfg.SV_TRACK = getInputFlag("Enable tracking?")
		cfg.SV_COUNT = getInputFlag("Enable counting?")

	return cfg

def getInputFlag(message):
	"""Quickly parse user input flags."""
	while 1:
		r = raw_input(message + " (Y/N): ")
		if r == "y" or r == "Y" or r == "yes" or r == "Yes":
			return True
		elif r == "n" or r == "N" or r == "no" or r == "No":
			return False

if __name__ == '__main__':
	# Get system parameters for initializing
	cfg = ewc()
	cfg = operationModeInit(cfg)

	# Initialize the tracker object
	main = expresswayCamera()

	if cfg.SV_RUN_LIVE:
		print("Running in Live mode.")
		main.loopLiveTest()
	else:
		print("Running in Test mode.")
		main.loop()

	# Make sure everything is cleaned up
	cv2.destroyAllWindows()

