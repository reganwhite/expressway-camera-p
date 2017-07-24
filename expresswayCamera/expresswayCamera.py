###### EXPRESSWAY CAMERA ######

# Declare the different libraries and what not that we might need
import numpy as np
import cv2
import time
import math
from tracker import tracker
from adjuster import adjuster
import socket
from counter import counter
import sys
from threading import Thread
#import picamera

# Counter resolution
COUNT_RES = 3
SV_TRACK = False
SV_COUNT = True

class expresswayCamera:
	"""Main Class. Handles iteration over images."""

	def __init__(self):
		"""Initialize variables."""
		# Get the system name to find the videofile
		name = socket.gethostname()

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

		# Initalize adjuster
		self.adj = adjuster()

		# Get frames for initialising background models
		success, frame = self.frameCapture.read()
		top, bot = self.adj.adjust(frame)

		if SV_TRACK:
			# Initialize the objects
			self.top_track = tracker("Top",top)
			self.bot_track = tracker("Bot",bot)

		if SV_COUNT:
			# Initialize the counters.
			self.top_count = counter(top, (COUNT_RES, COUNT_RES, 0.05), "Top")
			self.bot_count = counter(bot, (COUNT_RES, COUNT_RES, 0.05), "Bot")

		self.frame_time = time.time()

	def loop(self):
		"""Main loop of expresswayCam class"""
		# While there are still frames to be read
		count = 0
		float = 0
		while self.frameCapture.isOpened():
			count = count + 1
			# get the next frame\
			if count % 100 == 1:
				time1 = time.time()
			success, frame = self.frameCapture.read()
			if success:
				self.frame_time = time.time()
				top, bot = self.adj.adjust(frame)
				
				if SV_TRACK:
					self.top_track.track(top)
					self.bot_track.track(bot)

				if SV_COUNT:
					self.top_count.run(top)
					self.bot_count.run(bot)
			else:
				break
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

class frameGrabber:
	"""Grabs frames from the piCamera."""
	
	def __init__(self):
		"""Initialize variables."""
		# Settings initialised thanks to following stackexchange post by Dave Jones on 14th December, 2016
		# https://raspberrypi.stackexchange.com/questions/58871/pi-camera-v2-fast-full-sensor-capture-mode-with-downsampling
		self.cam = picamera()
		self.cam.sensor_mode = 4		# Full Frame, 2x2 binned mode
		self.cam.resolution = '120x90'	# Resolution for the Pi's GPU needs to downsample the input matrix to
		self.cam.framerate = 30			# Target framerate for the Raspberry Pi to aim for.

	def update(self):
		"""Updater for the settings which determine the Pi Camera's Operation."""
		# This it the groundwork for the function which will determine the operation of the Rasberry Pi camera in a number of
		# different environments.  For example, as the lighting conditions in the scene change so will settings such as shutter
		# speed and white balance, and this function will handle the configuring of those settings to ensure optimum opeartion
		# of the system.



def main():
	"""Main loop."""
	# Initialize the tracker object
	main = expresswayCam()
	main.loop()

	# Make sure everything is cleaned up
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()