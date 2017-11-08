<?php
	// Import anything necessary
	include('../include/helper.php');
	$con = include('db-connect-query.php');

	if (isset($_GET["typ"])) {
		// do quick basic auth
		$dir = mysqli_real_escape_string($con, $_GET["typ"]);

		if ($dir == 'count') {
			$speed = getLatest($con, "inboundCount", "dateTimeLOCAL");
		}
		elseif ($dir == 'speed') {
			$speed = getLatest($con, "inbound", "dateTimeLOCAL");
		}
		else {
			$speed = "Error reading post time.";
		}

		echo $speed;
	}
	else {
		echo "Error reading post time.";
	}
?>