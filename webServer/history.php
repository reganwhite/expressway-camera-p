<?php
	include_once('include/navbar.php');
	
	// Import anything necessary
	$con = include('data/db-connect-query.php');
	if (isset($_GET["type"])) {
		// do quick basic auth
		$typ = mysqli_real_escape_string($con, $_GET["type"]);
	}
	else
	{
		$typ = "error";
	}
?>

<!DOCTYPE html>
<html>
	<head>
		<script>
			document.getElementById("nav-hi").className = "active";
		</script>
	</head>
	<body>
		<div class="main">
			<div class="row" style="display: flex; flex: 1; justify-content: center; margin-bottom: 20px;">
				<?php
					if ($typ == "speed")
					{
						include_once("graph-1.php");
					}
					elseif ($typ == "flow")
					{
						include_once("graph-3.php");
					}
					else
					{
						echo "error.";
					}
				?>
			</div>
			<div class="row" style="display: flex; flex: 1; justify-content: center; margin-bottom: 20px;">
				<?php
					if ($typ == "speed")
					{
						include_once("graph-2.php");
					}
					elseif ($typ == "flow")
					{
						include_once("graph-4.php");
					}
					else
					{
						echo "error.";
					}
				?>
			</div>
		</div>
	</body>
</html>