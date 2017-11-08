<!DOCTYPE html>
<html>
	<body>
		<?php
			// Import anything necessary
			include('helper.php');
			$con = include('../data/db-connect-query.php');

			// Get up to date lane data
			$laneIn		= getLatest($con, "inbound", "speedLANE");
			$laneOut	= getLatest($con, "outbound", "speedLANE");
			
			// Split the delimited string
			$laneInSplit = explode('|',$laneIn);
			$laneOutSplit = explode('|',$laneOut);
			
			// Determine colours
			$speeds = array(10,60,55,20,60,55,10,5);
			
			// Iterate over the speed values and put them into the Speed object for processing
			for ($i = 0; $i < count($laneInSplit); $i++)
			{
				$speeds[$i] = floatval($laneInSplit[$i]);
			}
			for ($i = 0; $i < count($laneOutSplit); $i++)
			{
				$speeds[$i + 4] = floatval($laneOutSplit[$i]);
			}
		
			// Iterate over the speed values and determine Lane Colours
			$colour = array('','','','','','','','');
			for ($i = 0; $i < 8; $i++)
			{
				if($speeds[$i] > 30) {
					$colour[$i] = '#249b00';
				}
				elseif($speeds[$i] <= 30 && $speeds[$i] > 10) {
					$colour[$i] = '#e5db1b';
				}
				elseif($speeds[$i] <= 10 && $speeds[$i] > 5) {
					$colour[$i] = '#dd6000';
				}
				elseif($speeds[$i] <= 5) {
					$colour[$i] = '#9e0000';
				}
				elseif($speeds[$i] == 0) {
					$colour[$i] = '#3371d6';
				}
			}

			// Echo HTML to display
			echo '<canvas id="lanes" width="300" height="500"';
			echo '	style="border:0px solid #000000;">';
			echo '</canvas>';
			echo '<script>';
			echo '	var lanes = document.getElementById("lanes");';
			echo '	var ctx = lanes.getContext("2d");';
		
			// Set Constant for Lane Width
			$inc = 60;
		
			// Inbound Lanes
			for ($i = 0; $i < 4; $i++)
			{
				echo '	ctx.fillStyle = "'.$colour[$i].'";';
				echo '	ctx.fillRect(0,'.($inc * $i).',300,'.($i + 1) * $inc.');';
			}
			
			// Centre Strip
			echo '	ctx.fillStyle = "#1c1c1c";';
			echo '	ctx.fillRect(0,'.(4 * $inc).',300,'.(4 * $inc + 20).');';
			
			// Outbound Lanes
			for ($i = 0; $i < 4; $i++)
			{
				echo '	ctx.fillStyle = "'.$colour[4 + $i].'";';
				echo '	ctx.fillRect(0,'.(4 * $inc + 20 + $inc * $i).',300,'.(($i + 1) * $inc + 3 * $inc + 20).');';
			}
			echo 'ctx.lineWidth=5;';
			echo 'ctx.strokeStyle="#1c1c1c";';
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
		
			echo 'ctx.lineWidth=3;';
		
			for ($i = 0; $i < 4; $i++)
			{
				$x = 30;
				$y = 30 + $i * 60;
				
				echo 'ctx.moveTo('.$x.','.$y.');';
				echo 'ctx.lineTo('.($x - 10).','.($y - 10).');';
				echo 'ctx.stroke();';
				
				echo 'ctx.moveTo('.$x.','.($y - 1).');';
				echo 'ctx.lineTo('.($x - 10).','.($y + 10).');';
				echo 'ctx.stroke();';
			}
		
			for ($i = 0; $i < 4; $i++)
			{
				$x = 300 - 30;
				$y = 500 - 30 - $i * 60;
				
				echo 'ctx.moveTo('.$x.','.$y.');';
				echo 'ctx.lineTo('.($x + 10).','.($y - 10).');';
				echo 'ctx.stroke();';
				
				echo 'ctx.moveTo('.$x.','.($y - 1).');';
				echo 'ctx.lineTo('.($x + 10).','.($y + 10).');';
				echo 'ctx.stroke();';
			}
		
			echo 'ctx.font="30px Arial";';
			echo 'ctx.fillStyle="#FFFFFF";';
			echo 'ctx.lineWidth=4;';
		
			for ($i = 0; $i < 8; $i++)
			{
				if ($speeds[$i] == 0)
				{
					$speeds[$i] = "-";
				}
			}
		
			for ($i = 0; $i < 4; $i++)
			{
				$y = 40 + $i * 60;
				echo 'ctx.strokeText('.round($speeds[$i]).',40,'.$y.');';
				echo 'ctx.fillText('.round($speeds[$i]).',40,'.$y.');';
			}
			
			for ($i = 0; $i < 4; $i++)
			{
				$y = 300 + $i * 60;
				echo 'ctx.strokeText('.round($speeds[$i + 4]).',220,'.$y.');';
				echo 'ctx.fillText('.round($speeds[$i + 4]).',220,'.$y.');';
			}		
		
			echo '</script>';
		?>
		
	</body>
</html>