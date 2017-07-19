#import time

#class debugger:
#	"""DEBUGS THINGS!"""
#	def __init__(self):
#		self.t1 = 0
#		self.t2 = 0

#	def startTimer(self):
#		"""Start the timer!"""
#		self.t1 = time.time()

#	def stopTimer(self,name):
#		"""Stop the timer! Print duration to console with input 'name'!"""
#		self.t2 = time.time()
#		print('[{0}] = {1:2.3f}'.format((self.t2 - self.t1), name))

kappa = [1, 2, 3]
pride = [4, 5, 6]

print kappa + pride

print [x + y for x, y in zip(kappa, pride)]

print [float(x) / 3 for x in pride]