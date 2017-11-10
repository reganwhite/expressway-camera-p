# Expressway Camera
_Monitoring traffic conditions on the Riverside Expressway._

Visit the website at http://traffic.regandwhite.com.

See it running and how it works at https://www.youtube.com/playlist?list=PLSMRUyP8yFDCrO-2aIZO0zQ6YnVcLXMrY.

## What is this?
The Expressway Camera is a computer vision project by Regan White. The project was completed in 2017 for QUT's BEB801/BEB802 Assessment - under the supervision of Professor Peter Corke - with the intention of monitoring the traffic conditions of the Riverside Expressway. The system would run on a Raspberry Pi v3, operated from the 11th floor of QUT's S Block (overlooking the Riverside Expressway). Software to analyse traffic conditions was written in Python 2.7.9 with OpenCV 3.3.0, and would allow for the measuring of traffic speed on a lane-by-lane basis, traffic flow data (the number of vehicles travelling on the road), and other traffic information. This information is processed by the Raspberry Pi, before it is stored on both a web-server and MATLAB ThingSpeak.

Taking images from a small camera, the system uses feature detection and tracking to look at how objects are moving across the road. Counting the number of pixels travelled, the distance covered in meters can be found, and subsequently the speed of the vehicle calculated.

Traffic flow is found by looking for how many vehicles travel through the frame over a brief period. This is calculated by monitoring a thin vertical slice of the road, monitoring how many vehicles pass over it, and then extrapolating that out over a set time period.  Intensity (greyscale colour) of the road is monitored to detect vehicles.

This information is presented on the [project website](http://traffic.regandwhite.com).

## Replicating the System
_Replicating the system requires the following:_
- A Raspberry Pi 3 with a Pi Camera (v1 or v2), and a compiled copy of [OpenCV 3.3.0](https://github.com/opencv/opencv/releases/tag/3.3.0) for Python 2.7.9+
- A computer system, with a compiled copy of OpenCV 3.3.0 for Python 2.7.9+, along with a video file from which the algorithm can run

_As a base outline, the system also requires the following non-standard python packages:_
- requests
- datetime

_If run on a Raspberry Pi in a live environment, the software also requires:_
- picamera
- picamera.array

The Expressway Camera project does not support command line arguments, and inner workings can be editted in the **ewc** class.
