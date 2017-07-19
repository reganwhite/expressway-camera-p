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

		# Initiate our Frame Capture
		self.frameCapture = cv2.VideoCapture(CAP_VIDEOFILE)

		# Initalize adjuster
		self.adj = adjuster()

		# Get frames for initialising background models
		success, frame = self.frameCapture.read()
		top, bot = self.adj.adjust(frame)

		# Initialize the objects
		self.top = tracker("Top",top)
		self.bot = tracker("Bot",bot)

		self.top_count = counter(top)
		self.bot_count = counter(top)

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
				top, bot = self.adj.adjust(frame)
				self.top.track(top)
				self.bot.track(bot)
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


def main():
	"""Main loop."""
	# Initialize the tracker object
	main = expresswayCam()
	main.loop()

	# Make sure everything is cleaned up
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()