from sensor import sensor
import time

class counter:
	"""Handler for sensor class."""
	def __init__(self,frame,param):
		"""Initialize the handler."""
		# Set the dimensions of the base frame
		self.height, self.width = frame.shape

		# Get the sensor learning rate
		self.lr1 = param[2]

		# Prepare the input/output slices
		self.left = param[0]
		self.right = param[1]

		# Define where we want the slices to be
		self.x = 0

		# Initialize the blank lists
		self.sensor_l = []
		self.sensor_r = []

		# Ready status of the 
		self.readyStatusL = False
		self.readyStatusR = False
		self.runStatus = True

		# Store frames for use by the sensors
		self.frameBuffer = frame.copy()
		self.frameInUse = frame.copy()

		# Populate the lists
		for i in range(0, self.left - 1):
			self.sensor_l.append(sensor(x, 0.05, frame_))

		for i in range(0, self.right - 1):
			self.sensor_r.append(sensor(x, 0.05, frame_))

	def run(self, frame):
		"""Run the sensors.  Takes a frame as input."""
		while self.runStatus:
			if self.readyStatus:
				# Tell the object that we've used the buffered frame
				self.readyStatus = False

				# Run the updater
				self.update(frame)

			else:
				# Looks like we dont have anything to analyse yet.
				# Go to sleep for a moment to make sure we're not wasting clock cycles
				time.sleep(0.001)

	def push(self, frame):
		"""Pushes the latest frame to the object."""
		# Push the latest frame to buffer
		self.frameBuffer = frame.copy()

		# Set the status flag to ready
		self.readyStatus = True

	def getStatus(self):
		"""Returns the runtime status of the counter."""
		return self.readyStatus

	def setStatus(self, status):
		"""Sets the run status of the module to the input."""
		self.runStatus = status

	def update(self, frame):
		"""Operates the sensor instances."""
		# Initialize storage for 
		statusLeft = []
		statusRight = []

		# Take the input frame and start comparisons
		for i in range(0, self.left - 1):
			statusLeft.append(self.sensor_l[i].run(frame))
		for i in range(0, self.right - 1):
			statusRight.append(self.sensor_r[i].run(frame))
