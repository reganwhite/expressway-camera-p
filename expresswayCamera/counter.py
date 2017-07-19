from sensor import sensor

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

		# Populate the lists
		for i in range(0, self.left - 1):
			self.sensor_l.append(sensor(x, 0.05, frame_))

		for i in range(0, self.right - 1):
			self.sensor_r.append(sensor(x, 0.05, frame_))