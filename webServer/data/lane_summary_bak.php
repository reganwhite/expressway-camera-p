<?php
	// Import anything necessary
	

	// Get up to date lane data


	// Determine colours
	$speeds = array(10,60,55,20,60,55,10,5);

	for ($i = 0; $i < 8; $i++)
	{
		$speeds[$i] = rand(1,60);
	}
	$colour = array('','','','','','','','');
	for ($i = 0; $i < 8; $i++)
	{
		if($speeds[$i] > 30)	{
			$colour[$i] = '#249b00';
		}
		elseif($speeds[$i] <= 30 && $speeds[$i] > 10)	{
			$colour[$i] = '#e5db1b';
		}
		elseif($speeds[$i] <= 10 && $speeds[$i] > 5)	{
			$colour[$i] = '#dd6000';
		}
		elseif($speeds[$i] <= 5)	{
			$colour[$i] = '#9e0000';
		}
	}
	
	// Echo display code to display
	echo '<canvas id="lanes" width="300" height="500"';
	echo '	style="border:1px solid #000000;">';
	echo '</canvas>';
	echo '<script>';
	echo '	var lanes = document.getElementById("lanes");';
	echo '	var ctx = lanes.getContext("2d");';
	$inc = 60;
	for ($i = 0; $i < 4; $i++)
	{
		// Lane
		echo '	ctx.fillStyle = "'.$colour[$i].'";';
		echo '	ctx.fillRect(0,'.($inc * $i).',300,'.($i + 1) * $inc.');';
	}
	
	echo '	ctx.fillStyle = "#000000";';
	echo '	ctx.fillRect(0,'.(4 * $inc).',300,'.(4 * $inc + 20).');';

	for ($i = 0; $i < 4; $i++)
	{
		// Lane
		echo '	ctx.fillStyle = "'.$colour[4 + $i].'";';
		echo '	ctx.fillRect(0,'.(4 * $inc + 20 + $inc * $i).',300,'.(($i + 1) * $inc + 3 * $inc + 20).');';
	}
	echo 'ctx.lineWidth=5;';
	// Draw the line markings
	for ($i = 0; $i < 3; $i++)
	{
		if ($i == 0) {
			echo 'ctx.moveTo(0,'.$inc.');';
			echo 'ctx.lineTo(300,'.$inc.');';
			echo 'ctx.stroke();';
		}
		else {
			echo 'ctx.moveTo(40,'.$inc * ($i + 1).');';
			echo 'ctx.lineTo(100,'.$inc * ($i + 1).');';
			echo 'ctx.stroke();';
			
			echo 'ctx.moveTo(200,'.$inc * ($i + 1).');';
			echo 'ctx.lineTo(260,'.$inc * ($i + 1).');';
			echo 'ctx.stroke();';
		}
	}
	for ($i = 0; $i < 3; $i++)
	{
		if ($i != 2){
			echo 'ctx.moveTo(40,'.(4 * $inc + 20 + $inc * ($i + 1)).');';
			echo 'ctx.lineTo(100,'.(4 * $inc + 20 + $inc * ($i + 1)).');';
			echo 'ctx.stroke();';
			echo 'ctx.moveTo(200,'.(4 * $inc + 20 + $inc * ($i + 1)).');';
			echo 'ctx.lineTo(260,'.(4 * $inc + 20 + $inc * ($i + 1)).');';
			echo 'ctx.stroke();';
		}
		else {
			echo 'ctx.moveTo(45,'.(4 * $inc + 20 + $inc * ($i + 1)).');';
			echo 'ctx.lineTo(75,'.(4 * $inc + 20 + $inc * ($i + 1)).');';
			echo 'ctx.stroke();';
			echo 'ctx.moveTo(135,'.(4 * $inc + 20 + $inc * ($i + 1)).');';
			echo 'ctx.lineTo(165,'.(4 * $inc + 20 + $inc * ($i + 1)).');';
			echo 'ctx.stroke();';
			echo 'ctx.moveTo(225,'.(4 * $inc + 20 + $inc * ($i + 1)).');';
			echo 'ctx.lineTo(255,'.(4 * $inc + 20 + $inc * ($i + 1)).');';
			echo 'ctx.stroke();';
		}
	}
	echo '</script>';
?>