<?php
	// Initialize SQL connection
	$con = include('data/db-connect-query.php');
	
	$typ = mysqli_real_escape_string($con, $_GET['type']);

	// Parse inputs to make sure everything is valid
	$callback = mysqli_real_escape_string($con, $_GET['callback']);
	if (!preg_match('/^[a-zA-Z0-9_]+$/', $callback)) {
		die('Invalid callback name');
	}
	$start = mysqli_real_escape_string($con, $_GET['start']);
	if ($start && !preg_match('/^[0-9]+$/', $start)) {
		die("Invalid start parameter: $start");
	}
	$end = mysqli_real_escape_string($con, $_GET['end']);
	if ($end && !preg_match('/^[0-9]+$/', $end)) {
		die("Invalid end parameter: $end");
	}

	// Set start condition if none given
	if (!$end) $end = time();	// current time
	if (!$start) $start = 0;	// epoch

	// Table name, hardcoded at the moment, eventually will be input based
	if ($typ == "inb")
	{
		$table = "inboundCount";
	}
	else
	{
		$table = "outboundCount";
	}
	

	// scaling factor
	$scale = 100;

	// Firstly, we want to find out how many responses are in our time period
	$parse = "
		SELECT 
			COUNT(timeUNIX)		-- get the SQL count of the number of rows
		FROM $table
		WHERE timeUNIX BETWEEN '$start' AND '$end'
		ORDER BY timeUNIX
		LIMIT 0, 100000
	";

	// Get the number of rows
	$query = $con->query($parse);
	$results_array = array();
    while ($row = $query->fetch_assoc()) {
		$results_array[] = $row;
	}
	$resultCount =  $results_array[0]["COUNT(timeUNIX)"];
	
	// Find out what factor we want to apply modulus by
	$mod = round($resultCount / $scale);
	
	// If our modulus constant is less than 1. let it equal 1
	if ($mod == 0) $mod = 1;
	
	// Get our new query
	$parse = "
		SELECT 
			(timeUNIX) * 1000 AS timeUNIX,	-- scale the unix timestamps to milliseconds
			count,
			id
		FROM $table
		WHERE (timeUNIX BETWEEN '$start' AND '$end')
		AND (id%$mod=0)		-- apply modulus to decrease the number of data points
		ORDER BY timeUNIX
		LIMIT 0, $scale		-- limit to k data points, just incase mod fails
	";

	header('Content-Type: text/javascript');

	// Get the number of rows
	$query = $con->query($parse);
	$result = array();
    while ($row = $query->fetch_assoc()) {
		extract($row);
		
		$result[] = "[$timeUNIX,$speed,$id]";
	}
	
	echo "/* console.log(' start = $start, end = $end '); */";
	echo $callback ."([\n" . join(",\n", $result) ."\n]);";
	
?>