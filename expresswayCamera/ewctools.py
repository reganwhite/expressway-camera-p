import time
import numpy as np


class timer:
	"""This is a timer used to check how things are running!  Operates over a fixed number of iterations."""
	def __init__(self, ITERATIONS = 100, NAME = "BLNK", DISP_RPS = True, DISP_TIME = False, DISP_PERC = False, ROOT = False):
		# Parse inputs
		self.NAME = NAME				# What do we want to name this instance?
		self.DISP_RPS = DISP_RPS		# Do we want to display the output to console?
		self.DISP_TIME = DISP_TIME		# Do we want to display the output to console?
		self.DISP_PERC = DISP_PERC		# Do we want to display the output to console?
		self.ITERATIONS = ITERATIONS	# How many iterations are we expecting the tik to average over?
		self.ROOT = ROOT				# Is this the base timer?

		# Set up name for display
		self.NAME_FIX = "[" + self.NAME

		# Initialize timers
		self.t1 = 0
		self.t2 = 0
		self.t_tik = 0

		# Initialize counter
		self.count = 0

	def tik(self):
		"""Starts the counter."""
		tik = self.t1
		self.t1 = time.time()
		if self.count > 0:
			self.t_tik += self.t1 - tik
		

	def tok(self):
		"""Closes the tok and does some things"""
		self.count += 1
		self.t2 += float(time.time()) - float(self.t1)

		if self.count == self.ITERATIONS:
			if self.ROOT:
				print("------------------------------------------------")
			if self.DISP_RPS:
				# Print the output to console
				if self.t2 != 0:
					print('\r{0:>12}] = {1:11.4f} /s'.format(self.NAME_FIX, self.ITERATIONS/(self.t2)))
				else:
					print('\r{0:>12}] = {1:>12s}'.format(self.NAME_FIX, "undef/s"))
			if self.DISP_TIME:
				# Print the output to console
				if self.t2 != 0:
					print('\r{0:>12}] = {1:11.4f} s'.format(self.NAME_FIX, float(self.t2) / float(self.ITERATIONS) ))
				else:
					print('\r{0:>12}] = {1:>12s}'.format(self.NAME_FIX, "undef s"))
			if self.DISP_PERC:
				if self.t2 != 0:
					print('\r{0:>12}] = {1:11.4f} %'.format(self.NAME_FIX, float(self.t2) / float(self.t_tik) * 100))
				else:
					print('\r{0:>12}] = {1:>12s} %'.format(self.NAME_FIX, "0"))

			# Reset everything
			self.count	= 0
			self.t2		= 0
			self.t_tik	= 0
