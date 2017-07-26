import numpy as np
import cv2

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
		
		# Counter resolution
		cfg.COUNT_RES = 3
		cfg.SV_COUNT_UPDATE = 50
		cfg.SV_TRACK = True
		cfg.SV_COUNT = False
		cfg.SV_LIVE	= False

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
		cfg._LR1					= 0.1			# Learning rate for keypoint remover
		cfg._LR1_BASE				= 0.1
		cfg._LR2					= 0.01			# Learning rate for Speed Updater
		cfg._LR2_BASE				= 0.01
		cfg._FPS					= float(30)			# FPS of video file if being read from a video
		cfg._PPM_UNSCALED			= 195
		cfg._PPM					= float( cfg._PPM_UNSCALED / cfg.IM_BIN_SIZE / 3)	# Number of Pixels-Per-Meter
		cfg._MPS_to_KPH				= float(3.6)				# constant
		cfg._PixDiff				= 0.05
		cfg._FILTER_SPEED			= 30						# max concernable filter speed in kph

		#------------------------------------------------------------------------------------
		###### ------- adjuster settings ------- ######

		# Gaussian Blur
		cfg.GAUSS_KSIZE				= 0
		cfg.GAUSS_SIGMA_X			= 0
		cfg.GAUSS_SIGMA_Y			= 0

		#------------------------------------------------------------------------------------
		###### ------- counter settings ------- ######
		
		cfg.MAX_INT = 255

