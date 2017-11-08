<?php
	include_once('head.php');
?>

<!DOCTYPE html>
<html>
	<body>
		<nav class="navbar navbar-fixed-top">
			<div class="container-fluid" style="height: 60px">
				<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#bs-sidebar-navbar-collapse-1" style="z-index: 1000;">
					<span class="sr-only">Toggle navigation</span>
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
				</button>
				<a class="navbar-brand" href="home"><img src="include/images/car-1-small.png" alt="EW Traffic"></a>
			</div>
		</nav>
		<nav class="navbar navbar-inverse sidebar" role="navigation" style="background-color: #1a358c;">
			<div class="container-fluid">
				<!-- Collect the nav links, forms, and other content for toggling -->
				<div class="collapse navbar-collapse" id="bs-sidebar-navbar-collapse-1">
					<ul class="nav navbar-nav">
						<li id="nav-ho" class="inactive"><a href="home">Home<span style="font-size:16px;" class="pull-right hidden-xs showopacity glyphicon glyphicon-home"></span></a></li>
						<li id="nav-an" class="inactive"><a href="analytics">Analytics<span style="font-size:16px;" class="pull-right hidden-xs showopacity glyphicon glyphicon-stats"></span></a></li>
						<li id="nav-hi" class="dropdown">
							<a href="#" class="dropdown-toggle" data-toggle="dropdown">History <span class="caret"></span><span style="font-size:16px;" class="pull-right hidden-xs showopacity glyphicon glyphicon-calendar"></span></a>
							<ul class="dropdown-menu forAnimate" role="menu">
								<li><a href="history.php?type=speed">Traffic Speed<span style="font-size:16px;" class="pull-right hidden-xs showopacity glyphicon glyphicon-dashboard"></span></a></li>
								<li><a href="history.php?type=flow">Vehicle Count<span style="font-size:16px;" class="pull-right hidden-xs showopacity glyphicon glyphicon-road"></a></li>
							</ul>
						</li>
						<li id="nav-ab" class="inactive"><a href="about">About<span style="font-size:16px;" class="pull-right hidden-xs showopacity glyphicon glyphicon-education"></span></a></li>
					</ul>
				</div>
			</div>
		</nav>
	</body>
</html>