<?php

	// Finds the latest value in a desired column
	function getLatest($object, $table, $desired)
	{
		$query = $object->query("SELECT * FROM $table ORDER BY timeUNIX DESC LIMIT 0, 30");
        $results_array = array();
        while ($row = $query->fetch_assoc()) {
          $results_array[] = $row;
        }
		
		return $results_array[0][$desired];
	}

	// Connects to the mySQL Database
	function dbCon()
	{
		/*
		$user 		= "group11";  	// username
		$pass 		= "rfidd";  	// password
		$hostname 	= "localhost";	// server address on network
		*/

		$user		= "traffic_regan";	// username
		$pass		= "SJcOMPcXdJ#=";	// password
		$hostname	= "localhost";		// server address on network

		$con = mysqli_connect($hostname , $user, $pass);

		if (!$con) {
			echo "Error: Unable to connect to MySQL." . PHP_EOL;
			echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
			echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;
			exit;
		}
		else {
			return $con;
		}
	}

	/*
    // We use this function to validate the read ID's
	function checkRecord($value, $object) {
		if (!valueExists("enb345.user_student", $value, $object, "card_id")) {
			return '2';
		}
		else if (!checkTime("enb345.record", $value, $object)) {
			return '3';
		}
		else {
			return '1';
		}
	}

	// We use this function to validate the read ID's
	function checkNewUser($value, $object) {
		if (!valueExists("enb345.user_student", $value, $object, "card_id")) {
			return '1';
		}
		else {
			return '0';
		}
	}
	
	// Checks against the key table for existing tags
	function valueExists($table, $value, $object, $cell) {
		$result = $object->query("SELECT * FROM $table WHERE $cell = '$value'");
		
		if ($result->num_rows > 0) {
			return true;
		}
		else { return false; }
	}
	
	// Checks against the record table for previous reads
	function checkTime($table, $value, $object) {
		$result = $object->query("SELECT * FROM $table WHERE (student = '$value') AND (dateTime > NOW() - INTERVAL 4 SECOND)");
		
		if ($result->num_rows == 0) {
			return true;
		}
		else { return false; }
	}
	
	// Gets a desired cell from a searched row
	function getCell($table, $value, $object, $desired, $where) {
		$query = $object->query("SELECT * FROM $table WHERE $where = '$value'");
        $results_array = array();
        while ($row = $query->fetch_assoc()) {
          $results_array[] = $row;
        }
		
		return $results_array[0][$desired];
	}

    // Gets a name
	function getName($table, $value, $object, $desired) {
		$query = $object->query("SELECT * FROM $table WHERE card_id = '$value'");
        $results_array = array();
        while ($row = $query->fetch_assoc()) {
          $results_array[] = $row;
        }
		
		return $results_array[0][$desired];
	}
	
	// Gets a desired cell from the latest row
	function getLatestTime($table, $value, $object, $desired) {
		$query = $object->query("SELECT * FROM $table ORDER BY id DESC LIMIT 1");
        $results_array = array();
        while ($row = $query->fetch_assoc()) {
          $results_array[] = $row;
        }
		
		return $results_array[0][$desired];
	}
	*/
?>