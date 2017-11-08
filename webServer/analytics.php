<?php
	include_once('include/navbar.php');
?>

<!DOCTYPE html>
<html>
	<head>
		<script>
			document.getElementById("nav-an").className = "active";
		</script>
	</head>
	<body>
		<div class="main">
			<div class="row" style="display: flex; flex: 1; justify-content: center; margin-bottom: 20px;">
				<iframe width="450" height="250" style="border: 1px solid #cccccc;" src="http://thingspeak.com/channels/338458/charts/1?dynamic=true"></iframe>			
			</div>
			<div class="row" style="display: flex; flex: 1; justify-content: center; margin-bottom: 20px;">
				<iframe width="450" height="250" style="border: 1px solid #cccccc;" src="http://thingspeak.com/channels/338458/charts/2?dynamic=true"></iframe>
			</div>
			<div class="row" style="display: flex; flex: 1; justify-content: center; margin-bottom: 20px;">
				<iframe width="450" height="250" style="border: 1px solid #cccccc;" src="http://thingspeak.com/channels/338458/charts/3?dynamic=true"></iframe>			
			</div>
			<div class="row" style="display: flex; flex: 1; justify-content: center; margin-bottom: 20px;">
				<iframe width="450" height="250" style="border: 1px solid #cccccc;" src="http://thingspeak.com/channels/338458/charts/4?dynamic=true"></iframe>
			</div>
		</div>
	</body>
</html>