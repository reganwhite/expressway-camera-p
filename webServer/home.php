<?php
	// Include the navbar and sidebar
	include_once('include/navbar.php');
?>

<!DOCTYPE html>
<html>
	<head>
		<script>
			document.getElementById("nav-ho").className = "active";
		</script>
		<script>
			$(function(){
				$("#lane-data").load("include/lane_summary.php");
				
				$.get('data/get_speed.php?dir=inbound', function(response) {
					inSP = parseInt(response);
					
					if(inSP > 30) {
						document.getElementById("in-c").style.backgroundColor = "#249b00";
					}
					else if(inSP <= 30 && inSP > 10) {
						document.getElementById("in-c").style.backgroundColor = "#e5db1b";
					}
					else if(inSP <= 10 && inSP > 5) {
						document.getElementById("in-c").style.backgroundColor = "#dd6000";
					}
					else if(inSP <= 5) {
						document.getElementById("in-c").style.backgroundColor = "#9e0000";
					}
					
					$("#in-s").html(inSP);
				});
				
				$.get('data/get_speed.php?dir=outbound', function(response) {
					ouSP = parseInt(response);
					
					if(ouSP > 30) {
						document.getElementById("out-c").style.backgroundColor = "#249b00";
					}
					else if(ouSP <= 30 && ouSP > 10) {
						document.getElementById("out-c").style.backgroundColor = "#e5db1b";
					}
					else if(ouSP <= 10 && ouSP > 5) {
						document.getElementById("out-c").style.backgroundColor = "#dd6000";
					}
					else if(ouSP <= 5) {
						document.getElementById("out-c").style.backgroundColor = "#9e0000";
					}

					$("#out-s").html(ouSP);
				});
				
				$.get('data/get_count.php?dir=inbound', function(response) {
					inCO = parseInt(response);
					$("#in-count").html(inCO);
				});
				
				$.get('data/get_count.php?dir=outbound', function(response) {
					ouCO = parseInt(response);
					$("#out-count").html(ouCO);
				});
				
				$.get('data/get_datetime.php?typ=speed', function(response) {
					sp = response;
					document.getElementById("trafficSpeed").textContent = sp;
				});
				
				$.get('data/get_datetime.php?typ=count', function(response) {
					co = response;
					document.getElementById("trafficCount").textContent = co;
				});
				
			});
			var t = 15;
			var refreshTimer = setInterval(function(){
				t = t - 1;
				document.getElementById("refreshTime").textContent = t;
				if(t <= 0)
					clearInterval(refreshTimer);
			}, 1000);
			setInterval(function(){
				$("#lane-data").load("include/lane_summary.php");
				
				$.get('data/get_speed.php?dir=inbound', function(response) {
					inSP = parseInt(response);
					
					if(inSP > 30) {
						document.getElementById("in-c").style.backgroundColor = "#249b00";
					}
					else if(inSP <= 30 && inSP > 10) {
						document.getElementById("in-c").style.backgroundColor = "#e5db1b";
					}
					else if(inSP <= 10 && inSP > 5) {
						document.getElementById("in-c").style.backgroundColor = "#dd6000";
					}
					else if(inSP <= 5) {
						document.getElementById("in-c").style.backgroundColor = "#9e0000";
					}
					
					$("#in-s").html(inSP);
				});
				
				$.get('data/get_speed.php?dir=outbound', function(response) {
					ouSP = parseInt(response);
					
					if(ouSP > 30) {
						document.getElementById("out-c").style.backgroundColor = "#249b00";
					}
					else if(ouSP <= 30 && ouSP > 10) {
						document.getElementById("out-c").style.backgroundColor = "#e5db1b";
					}
					else if(ouSP <= 10 && ouSP > 5) {
						document.getElementById("out-c").style.backgroundColor = "#dd6000";
					}
					else if(ouSP <= 5) {
						document.getElementById("out-c").style.backgroundColor = "#9e0000";
					}

					$("#out-s").html(ouSP);
				});
				
				$.get('data/get_count.php?dir=inbound', function(response) {
					inCO = parseInt(response);
					$("#in-count").html(inCO);
				});
				
				$.get('data/get_count.php?dir=outbound', function(response) {
					ouCO = parseInt(response);
					$("#out-count").html(ouCO);
				});
				
				$.get('data/get_datetime.php?typ=speed', function(response) {
					sp = response;
					document.getElementById("trafficSpeed").textContent = sp;
				});
				
				$.get('data/get_datetime.php?typ=count', function(response) {
					co = response;
					document.getElementById("trafficCount").textContent = co;
				});
				
				var t = 15;
				var refreshTimer = setInterval(function(){
					t = t - 1;
					document.getElementById("refreshTime").textContent = t;
					if(t <= 0)
						clearInterval(refreshTimer);
				}, 1000);
			}, 15000);
		</script>
		
		<script type="text/javascript"></script>
		
		<style>
			.speed-title{
				display: flex;
				font-size: 25px;
				align-items: center;
				text-align: right;
				height: 85px;
				width: 150px;
				float: none;
				margin-right: 10px;
			}
			.speed{
				text-align: center;
				vertical-align: middle;
				font-size: 60px;
				width: 100px;
				height: 85px;
				margin: 0 auto;
				float: none;
				margin-right: -15px;
				margin-left: -10px;
			}
			.speed-info{
				display: flex;
				font-size: 20px;
				align-items: center;
				text-align: center;
				height: 85px;
				width: 65px;
				float: none;
				margin-right: -7px;
			}
			.count{
				text-align: center;
				vertical-align: middle;
				font-size: 48px;
				width: 90px;
				height: 85px;
				margin: 0 auto;
				float: none;
				padding-top: 12px;
			}
			.count-info{
				display: flex;
				font-size: 20px;
				align-items: center;
				text-align: center;
				height: 85px;
				width: 85px;
				float: none;
				margin-right: -7px;
			}
			.col-xs-1{
				width: auto;
				padding-left: 5px;
				padding-right: 5px;
			}
			.col-xs-2{
				width: auto;
				padding-left: 0px;
				padding-right: 0px;
			}
		</style>
	</head>
	<body>
		<div class="main">
			<div class="row">
				<div class="col">
					<div class="row" id="in-b" style="display: flex; flex: 1; justify-content: center;">
						<div class="col-xs-1">
							<div class="speed-title"style="height: 40px; margin-bottom: 5px; text-align: center; width: auto;">Riverside Expressway, Brisbane</div>
						</div>
					</div>
					<div class="row">
						<div class="col" style="text-align: center; margin-top: 10px; margin-bottom: 30px;">
							<p>Don't understand what's going on? <a href="about">Click here!</a></p>
						</div>
					</div>
					<div class="row" id="in-b" style="display: flex; flex: 1; justify-content: center;">
						<div class="col-xs-1">
							<div class="speed-title"style="height: 40px; margin-bottom: 5px; text-align: center; width: auto;">Traffic Information</div>
						</div>
					</div>
					<div class="row" id="in-b" style="display: flex; flex: 1; justify-content: center;">
						<div class="col-xs-1">
							<div class="speed-title" style="padding-left: 28px;">INBOUND:</div>
						</div>
						<div class="col-xs-2" id="in-c">
							<div class="col-xs-1">
								<div class="speed" id="in-s">00</div>
							</div>
							<div class="col-xs-1" style="padding-left: -20px;">
								<div class="speed-info">km/hr </div>
							</div>
						</div>
						<div class="col-xs-2" id="in-c" style="background-color: #3371d6">
							<div class="col-xs-1">
								<div class="count" id="in-count">000</div>
							</div>
							<div class="col-xs-1" style="padding-left: -20px;">
								<div class="count-info">cars/min </div>
							</div>
						</div>
					</div>
					<div class="row" id="out-b" style="display: flex; flex: 1; justify-content: center;">
						<div class="col-xs-1">
							<div class="speed-title">OUTBOUND:</div>
						</div>
						<div class="col-xs-2" id="out-c">
							<div class="col-xs-1">
								<div class="speed" id="out-s">00</div>
							</div>
							<div class="col-xs-1" style="padding-left: -20px;">
								<div class="speed-info" style="padding-left: -20px;">km/hr</div>
							</div>
						</div>
						<div class="col-xs-2" id="out-c" style="background-color: #3371d6">
							<div class="col-xs-1">
								<div class="count" id="out-count">000</div>
							</div>
							<div class="col-xs-1" style="padding-left: -20px;">
								<div class="count-info" style="padding-left: -20px;">cars/min</div>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div class="row">
				<div class="row" id="in-b" style="display: flex; flex: 1; justify-content: center;">
						<div class="col-xs-1">
							<div class="speed-title"style="height: 40px; margin-bottom: 5px; margin-top: 25px; text-align: center; width: auto;">Lane Speed Summary</div>
						</div>
					</div>
				<div class="row">
					<div class="col" style="text-align: center; margin-top: 10px;">
						<div id="lane-data"></div>
						<p>Data will update in <span id="refreshTime">15 </span> seconds...</p>
						<p>Traffic speed recorded at <span id="trafficSpeed">-</span></p>
						<p>Traffic flow rate recorded at <span id="trafficCount">-</span></p>
					</div>
				</div>
			</div>
		</div>
	</body>
</html>