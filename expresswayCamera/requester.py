# Import necessary packages
import requests
from threading import Thread
import time
from ewc import ewc

class requester:
	"""HTTP Request Class: This class is used to transfer data from the system to the web server via HTTP requests."""

	def __init__(self, urlP1, target):
		"""Initialize the class information."""
		# Import settings class
		self.cfg = ewc()

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
		self.ts_update_url	= "https://api.thingspeak.com/update"


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
	
	def ts_poster(self):
		"""Posts information to the thingspeak channel."""
		r = requests.get(self.ts_update_url, params = {'api_key':self.speedStrComb, 'field1':self.speedStrUNIX, 'field1':self.speedStrLane})
