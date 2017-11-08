<?php
	$con = include('db-connect-entry.php');
	mysqli_query($con, "SET time_zone = '+10:00'");
	//$input_dir = mysqli_real_escape_string($con, $_GET["dir"]);

	// Check to see if the requests exist
	// The requests exist, 
	if (isset($_GET["sp"]) && isset($_GET["t"]) && isset($_GET["l"]) && isset($_GET["dir"]))
	{
		// Get the target
		$input_t = mysqli_real_escape_string($con, $_GET["dir"]);
		if ($input_t == "Top") {
			$target = "inbound";
		}
		elseif ($input_t == "Bot") {
			$target = "outbound";
		}
		
		// Parse the inputs with escape strings to prevent SQL injection
		$input_a = mysqli_real_escape_string($con, $_GET["sp"]);
		$input_b = mysqli_real_escape_string($con, $_GET["t"]);
		$input_c = mysqli_real_escape_string($con, $_GET["l"]);
		
		
		// Explode input strings to separate dilimited varchars
		$split_input_a = explode(',',$input_a);
		$split_input_b = explode(',',$input_b);
		$split_input_c = explode(',',$input_c);
		
		echo "Example: ".$split_input_c[0]."<br>";

		// For the 4 inputs sent 
		for ($i = 0; $i < count($split_input_a); $i++)
		{
			// Prepare the SQL statement
			echo date("Y-m-d H-i-s",$split_input_b[$i]);
			
			$statement = "INSERT INTO `traffic-data`.".$target." (speed,timeUNIX,dateTimeLOCAL,speedLANE) VALUES (".$split_input_a[$i].",".$split_input_b[$i].",'".date("Y-m-d H-i-s",$split_input_b[$i])."',\"".$split_input_c[$i]."\")";
			echo $statement."<br>";
			// Execute SQL statement
			mysqli_query($con, $statement) or die(mysqli_error($con));
		}
		echo "GREAT SUCCESS!<br>";
	}
	// Else, the request does not exist
	else
	{
		echo "Something seems to have gone wrong.<br>";
	}
	
?>