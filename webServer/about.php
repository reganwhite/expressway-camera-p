<?php
	include_once('include/navbar.php');
?>

<!DOCTYPE html>
<html>
	<head>
		<script>
			document.getElementById("nav-ab").className = "active";
		</script>
	</head>
	<body>
		<div class="main">
			<div class="row">
				<div class="col">
					<h2 id="sec0">Expressway Camera</h2>
					<hr class="col-md-12">
					The Expressway Camera is a computer vision project by Regan White.  The project was completed in 2017 for QUT's BEB801/BEB802 Assessment - under the supervision of Professor Peter Corke - with the intention of monitoring the traffic conditions of the Riverside Expressway.  The system would run on a Raspberry Pi v3, operated from the 11th floor of QUT's S Block (overlooking the Riverside Expressway).  Software to analyse traffic conditions was written in Python 2.7.9 with OpenCV 3.3.0, and would allow for the measuring of traffic speed on a lane-by-lane basis, traffic flow data (the number of vehicles travelling on the road), and other traffic information.  This information is processed by the Raspberry Pi, before it is stored on both a web-server and MATLAB ThingSpeak.
					
					<div class="row">
						<div class="col-md-2" style="margin-bottom: 15px; margin-top: 10px"></div>
						<div class="col-md-4" style="margin-bottom: 15px; margin-top: 10px"><img src="include/images/ewc_setup.jpg" class="img-responsive center-block"></div>
						<div class="col-md-4" style="margin-bottom: 15px; margin-top: 10px"><img src="include/images/expressway.jpg" class="img-responsive center-block"></div>
						<div class="col-md-2" style="margin-bottom: 15px; margin-top: 10px"></div>
					</div>
					
					<h2 id="sec1">How It Works</h2>
					<h3>Traffic Speed</h3>
					<p>
					Taking images from a small camera, the system uses feature detection and tracking to look at how objects are moving across the road. Counting the number of pixels travelled, the distance covered in meters can be found, and subsequently the speed of the vehicle calculated.
					</p>
					<div class="row">
						<div class="col" style="margin-bottom: 15px; margin-top: 10px"><img src="include/images/feature_matching.jpg" class="img-responsive center-block"></div>
					</div>
					<p>
					This speed information is found at the top of the home page, as shown in the figure below (with speeds highlighted in red).
					</p>
					<div class="row">
						<div class="col" style="margin-bottom: 15px; margin-top: 10px"><img src="include/images/speed_updater.jpg" class="img-responsive center-block"></div>
					</div>
					<p>					
					From this, we can also find the individual speed of cars in each lane, by iterating over the image and looking at which lane the features reside in.
					</p>
					<div class="row">
						<div class="col" style="margin-bottom: 15px; margin-top: 10px"><img src="include/images/lane_split.jpg" class="img-responsive center-block"></div>
					</div>
					<p>
					This speed information is shown on the home page, just below the average speed image.  The image first image below on the left shows what a typical lane speed summary could look like.  The second image below shows what the lane summary image represents; the road from a birds eye view.  The arrows in the lanes show the direction of traffic flow, with upper four lanes represent in "Inbound" traffic (heading north into the city), whereas the bottom four lanes represent the "Outbound" traffic (heading south away from the city).  The number shown in each lane tells us the average vehicle speed in that lane in km/hr.
					</p>
					<div class="row">
						<div class="col-md-2" style="margin-bottom: 15px; margin-top: 10px"></div>
						<div class="col-md-4" style="margin-bottom: 15px; margin-top: 10px"><img src="include/images/lane_summary_demo.png" class="img-responsive center-block"></div>
						<div class="col-md-4" style="margin-bottom: 15px; margin-top: 10px"><img src="include/images/lane_summary_location.jpg" class="img-responsive center-block"></div>
						<div class="col-md-2" style="margin-bottom: 15px; margin-top: 10px"></div>
					</div>
					
					<h3>Traffic Flow</h3>
					<p>
					Traffic flow is found by looking for how many vehicles travel through the frame over a brief period.  This is calculated by monitoring a thin vertical slice of the road, monitoring how many vehicles pass over it, and then extrapolating that out over a set time period.  The figure below demonstrates how the intensity (greyscale colour) of the road is monitored to detect a vehicle.
					</p>
					<div class="row">
						<div class="col" style="margin-bottom: 15px; margin-top: 10px"><img src="include/images/counter_theory.jpg" class="img-responsive center-block"></div>
					</div>
					<p>
					This traffic flow information is found at the top of the home page, as shown in the figure below (with vehicle count per minute highlighted in red).
					</p>
					<div class="row">
						<div class="col" style="margin-bottom: 15px; margin-top: 10px"><img src="include/images/count_updater.jpg" class="img-responsive center-block"></div>
					</div>
					<h3>Source Code</h3>
					<p>
					Python source code can be found on github, at <a href="https://github.com/reganwhite/expressway-camera-p">https://github.com/reganwhite/expressway-camera-p</a>.
					</p>
					<div style="margin-bottom: 50px"></div>
					<h2>Acknowledgements</h3>
					<p>
					My many thanks...
					</p>
					<p>
					To Professor Peter Corke, for your guidance and assistance throughout the year, and for making this a very enjoyable experience.
					</p>
					<p>
					To Ben Pederson, for constantly reminding me that the reason why my software didn't work was in fact <i>not</i> because of an error in OpenCV's source code.
					</p>
					<p>
					To Ben Pederson, Logan Payne, Cameron Hancock, Blue Carter, Kalen Parker, Jayme-lee and Bek Groer, for proof-reading my terribly written work.
					</p>
					<p>
					To the Raspberry Pi for demonstrating its exceptional WiFi stability on presentation day.
					</p>
					<div class="col" style="margin-bottom: 15px; margin-top: 0px;"><img src="include/images/wifi_crash.jpg" class="img-responsive center-block"></div>
					<div style="margin-bottom: 200px"></div>
					<div class="row">
						
					</div>
				</div>
			</div>
		</div>
	</body>
</html>