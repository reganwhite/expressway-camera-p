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
		<script src="https://code.highcharts.com/stock/highstock.js"></script>
		<script src="https://code.highcharts.com/stock/modules/exporting.js"></script>

		<link rel="stylesheet prefetch" href="//fonts.googleapis.com/css?family=Lato&amp;subset=latin,latin-ext">
		
		<script type="text/javascript" src="js/moment.min.js"></script>
		<script type="text/javascript" src="js/transition.js"></script>
		<script type="text/javascript" src="js/collapse.js"></script>
		<script type="text/javascript" src="js/bootstrap-datetimepicker.min.js"></script>
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/4.17.47/css/bootstrap-datetimepicker.min.css" />
	</head>

	<style>
		.navbar-brand {
			position: absolute;
			width: 127px;
			height: 50px;
			margin-top: 6px;
			margin-left: -32px !important; /*-64px*/
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
			min-height: 0px;
			margin-bottom: 0px;
			margin-left: 0px;
			margin-right: 0px;
			border: 0px solid transparent;
			background-color: #1a358c;
			z-index: 1000;
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
		
		.navbar-fixed-top .navbar-toggle:hover, .navbar-fixed-top .navbar-toggle:focus {
			background-color: #3371d6;
		}
		
		.navbar-fixed-top .navbar-toggle .icon-bar {
			background-color: #fff;
		}
		
		.navbar-fixed-top .navbar-toggle {
			border-color: #fff;
			margin-top: 13px;
			margin-bottom: 13px;
			margin-right: 0px;
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
			padding: 80px 5% 0 5%;
			z-index: 10;
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
</html>