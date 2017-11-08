<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8"/>
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>EWTraffic</title>

		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>

		<link rel="stylesheet" href="css/bootstrap.min.css">

		<link rel="stylesheet" href="css/bootstrap-theme.min.css">

		<script src="js/bootstrap.js"></script>

		<link rel="stylesheet prefetch" href="//fonts.googleapis.com/css?family=Lato&amp;subset=latin,latin-ext">
		
		<script type="text/javascript" src="js/moment.min.js"></script>
		<script type="text/javascript" src="js/transition.js"></script>
		<script type="text/javascript" src="js/collapse.js"></script>
		<script type="text/javascript" src="js/bootstrap-datetimepicker.min.js"></script>
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/4.17.47/css/bootstrap-datetimepicker.min.css" />
		<script>
			$(function(){
				$("#div1").load("lane_summary.php");
			});
			var t = 15;
			var refreshTimer = setInterval(function(){
				t = t - 1;
				document.getElementById("refreshTime").textContent = t;
				if(t <= 0)
					clearInterval(refreshTimer);
			}, 1000);
			setInterval(function(){
				$("#div1").load("lane_summary.php");
				var t = 15;
				var refreshTimer = setInterval(function(){
					t = t - 1;
					document.getElementById("refreshTime").textContent = t;
					if(t <= 0)
						clearInterval(refreshTimer);
				}, 1000);
			}, 15000);
		</script>
		<script type="text/javascript">
			$(function () {
				$('#dateStart').datetimepicker();
				$('#dateEnd').datetimepicker({
					useCurrent: false //Important! See issue #1075
				});
				$("#dateStart").on("dp.change", function (e) {
					$('#dateEnd').data("DateTimePicker").minDate(e.date);
				});
				$("#dateEnd").on("dp.change", function (e) {
					$('#dateStart').data("DateTimePicker").maxDate(e.date);
				});
			});
		</script>

		<script type="text/javascript"></script>
	</head>

	<style>
		.navbar-brand {
			position: absolute;
			width: 127px;
			height: 50px;
			margin-top: 6px;
			margin-left: 38px !important; /*-64px*/
			padding: 0;
			text-align: center;
		}
		box-center {
			margin: 0 auto;
			float: none;
			text-align: right;
		}
		.navbar {
			position: fixed;
			text-align: center;
			min-height: 20px;
			margin-bottom: 0px;
			margin-left: 0px;
			margin-right: 0px;
			border: 0px solid transparent;
			background-color: #1a358c;
		}
		body {
			background-color: #f4f4f4;
			padding-top: 0px;
			padding-bottom: 0px;
			color: #000;
		}
		body,html{
			height: 100%;
		}
		
		.navbar-inverse {
			background-color: #1a358c;
			background-image: none;
			color: #f4f4f4;
			font-size: 125%;
			margin-top: 60px;
		}
		
		.navbar-inverse .navbar-nav>.active>a, .navbar-inverse .navbar-nav>.active>a:focus, .navbar-inverse .navbar-nav>.active>a:hover {
			color: #f4f4f4;
			background-color: #061238;
			background-image: none;
		}
		
		.navbar-inverse .navbar-nav>.open>a, .navbar-inverse .navbar-nav>.open>a:focus, .navbar-inverse .navbar-nav>.open>a:hover {
			background-image: none;
    		color: #f4f4f4;
    		background-color: #2f55ce;
		}
		
		.navbar-inverse .navbar-nav>li>a {
			color: #f4f4f4;
		}
		
		
		.navbar-inverse .navbar-nav>li>a:hover {
			color: #7c7c7c;
		}

		/* remove outer padding */
		.main .row{
			padding: 0px;
			margin: 0px;
		}

		/*Remove rounded coners*/

		nav.sidebar.navbar {
			border-radius: 0px;
		}

		nav.sidebar, .main{
			-webkit-transition: margin 200ms ease-out;
			-moz-transition: margin 200ms ease-out;
			-o-transition: margin 200ms ease-out;
			transition: margin 200ms ease-out;
		}

		/* Add gap to nav and right windows.*/
		.main{
			padding: 70px 5% 0 5%;
		}

		/* .....NavBar: Icon only with coloring/layout.....*/

		/*small/medium side display*/
		@media (min-width: 768px) {

			/*Allow main to be next to Nav*/
			.main{
				position: absolute;
				width: calc(100% - 40px); /*keeps 100% minus nav size*/
				margin-left: 40px;
				float: right;
			}

			/*lets nav bar to be showed on mouseover*/
			nav.sidebar:hover + .main{
				margin-left: 200px;
			}

			/*Center Brand*/
			nav.sidebar.navbar.sidebar>.container .navbar-brand, .navbar>.container-fluid .navbar-brand {
				margin-left: 0px;
			}
			/*Center Brand*/
			nav.sidebar .navbar-brand, nav.sidebar .navbar-header{
				text-align: center;
				width: 100%;
				margin-left: 0px;
			}

			/*Center Icons*/
			nav.sidebar a{
				padding-right: 13px;
			}
			
			/*adds border top to first nav box */
			nav.sidebar .navbar-nav > li:first-child{
				border-top: 1px #f4f4f4 solid;
			}

			/*adds border to bottom nav boxes*/
			nav.sidebar .navbar-nav > li{
				border-bottom: 1px #f4f4f4 solid;
			}

			/* Colors/style dropdown box*/
			nav.sidebar .navbar-nav .open .dropdown-menu {
				position: static;
				float: none;
				width: auto;
				margin-top: 0;
				background-color: transparent;
				border: 0;
				-webkit-box-shadow: none;
				box-shadow: none;
			}

			/*allows nav box to use 100% width*/
			nav.sidebar .navbar-collapse, nav.sidebar .container-fluid{
				padding: 0 0px 0 0px;
			}

			/*colors dropdown box text */
			.navbar-inverse .navbar-nav .open .dropdown-menu>li>a {
				color: #f4f4f4;
			}

			/*gives sidebar width/height*/
			nav.sidebar{
				width: 200px;
				height: 100%;
				margin-left: -160px;
				float: left;
				z-index: 8000;
				margin-bottom: 0px;
			}

			/*give sidebar 100% width;*/
			nav.sidebar li {
				width: 100%;
			}

			/* Move nav to full on mouse over*/
			nav.sidebar:hover{
				margin-left: 0px;
			}
			/*for hiden things when navbar hidden*/
			.forAnimate{
				opacity: 0;
			}
		}

		/* .....NavBar: Fully showing nav bar..... */

		@media (min-width: 1330px) {

			/*Allow main to be next to Nav*/
			.main{
				width: calc(100% - 200px); /*keeps 100% minus nav size*/
				margin-left: 200px;
			}

			/*Show all nav*/
			nav.sidebar{
				margin-left: 0px;
				float: left;
			}
			/*Show hidden items on nav*/
			nav.sidebar .forAnimate{
				opacity: 1;
			}
		}

		nav.sidebar .navbar-nav .open .dropdown-menu>li>a:hover, nav.sidebar .navbar-nav .open .dropdown-menu>li>a:focus {
			color: #666666;
			background-color: #f4f4f4 !important;
			background-image: none;
		}

		nav:hover .forAnimate{
			opacity: 1;
		}
		section{
			padding-left: 15px;
		}
	</style>

	<body>
		<nav class="navbar navbar-fixed-top">
			<div class="container-fluid" style="height: 60px">
				<a class="navbar-brand" href="home"><img src="include/images/car-1-small.png" alt="EW Traffic"></a>
			</div>
		</nav>
		<nav class="navbar navbar-inverse sidebar" role="navigation" style="background-color: #1a358c;">
			<div class="container-fluid">
				<!-- Collect the nav links, forms, and other content for toggling -->
				<div class="collapse navbar-collapse" id="bs-sidebar-navbar-collapse-1">
					<ul class="nav navbar-nav">
						<li class="active"><a href="home">Home<span style="font-size:16px;" class="pull-right hidden-xs showopacity glyphicon glyphicon-home"></span></a></li>
						<li ><a href="analytics">Analytics<span style="font-size:16px;" class="pull-right hidden-xs showopacity glyphicon glyphicon-stats"></span></a></li>
						<li class="dropdown">
							<a href="#" class="dropdown-toggle" data-toggle="dropdown">History <span class="caret"></span><span style="font-size:16px;" class="pull-right hidden-xs showopacity glyphicon glyphicon-calendar"></span></a>
							<ul class="dropdown-menu forAnimate" role="menu">
								<li><a href="#">Traffic Speed<span style="font-size:16px;" class="pull-right hidden-xs showopacity glyphicon glyphicon-dashboard"></span></a></li>
								<li><a href="#">Vehicle Count<span style="font-size:16px;" class="pull-right hidden-xs showopacity glyphicon glyphicon-road"></a></li>
							</ul>
						</li>
						<li ><a href="about">About<span style="font-size:16px;" class="pull-right hidden-xs showopacity glyphicon glyphicon-education"></span></a></li>
					</ul>
				</div>
			</div>
		</nav>
		<div class="main">
			<div class="row">
				<div class="col" style="text-align: center;">
					<div id="div1"></div>
					<p> The figure will refresh in <span id="refreshTime">15 </span> seconds...</p>
				</div>
				<div class="col">
					<br>
					<h2 id="sec0">Content</h2>
					<hr class="col-md-12">
					Rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae 
					dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia cor magni dolores 
					eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, 
					sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. 
					Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut.              
					Rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae 
					dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia cor magni dolores 
					eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, 
					sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. 
					Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut!

					<h2 id="sec1">Content</h2>
					<p>
					Rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae 
					dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut.
					</p>
					<div class="row">
					  <div class="col-md-6">
						<div class="panel panel-default">
						  <div class="panel-heading"><h3>Hello.</h3></div>
						  <div class="panel-body">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis pharetra varius quam sit amet vulputate. 
						  Quisque mauris augue, molestie tincidunt condimentum vitae, gravida a libero. Aenean sit amet felis 
						  dolor, in sagittis nisi. Sed ac orci quis tortor imperdiet venenatis. Duis elementum auctor accumsan. 
						  Aliquam in felis sit amet augue.
						  </div>
						</div>
					  </div>
					  <div class="col-md-6">
						  <div class="panel panel-default">
						  <div class="panel-heading"><h3>Hello.</h3></div>
						  <div class="panel-body">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis pharetra varius quam sit amet vulputate. 
						  Quisque mauris augue, molestie tincidunt condimentum vitae, gravida a libero. Aenean sit amet felis 
						  dolor, in sagittis nisi. Sed ac orci quis tortor imperdiet venenatis. Duis elementum auctor accumsan. 
						  Aliquam in felis sit amet augue.
						  </div>
						</div>
					  </div>  
					</div>

					<hr>

					<h2 id="sec2">Section 2</h2>
					<p>
					Rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae 
					dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia cor magni dolores 
					eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, 
					sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. 
					Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut!
					</p>
					<div class="row">
						<div class="col-md-4"><img src="//placehold.it/300x300" class="img-responsive"></div>
						<div class="col-md-4"><img src="//placehold.it/300x300" class="img-responsive"></div>
						<div class="col-md-4"><img src="//placehold.it/300x300" class="img-responsive"></div>
					</div>

					<h3 id="sec2a">Section 2 a</h3>
					<p>
					Rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae 
					dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia cor magni dolores.
					Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, 
					sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. 
					  Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia cor magni dolores 
					eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, 
					sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. 
					Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut!
					  <br><br>
					</p>

					<h3 id="sec2b">Section 2 b</h3>
					<p>
					Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia cor magni dolores. Nemo enim ipsam voluptatem quia voluptas 
					sit aspernatur aut odit aut fugit, sed quia cor magni dolores. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, 
					sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. 
					  Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia cor magni dolores 
					eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, 
					sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. 
					Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut!
					sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem.<br><br>
					</p>


					<hr>

					<h2 id="sec3">Section 3</h2>
					Images are responsive sed @mdo but sum are more fun peratis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, 
					totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae 
					dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia cor magni dolores 
					eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, 
					sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. 
					Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut!!<br><br>


					<hr>

					<h2 id="sec4">Section 4</h2>
					Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, 
					totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae 
					dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia cor magni dolores 
					eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, 
					sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. 
					Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut<br><br>
				</div>
			</div>
		</div>
	</body>
</html>