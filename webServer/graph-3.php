<!DOCTYPE HTML>
<html>
	<head>
		<div id="container-a" style="height: 400px; min-width: 310px; max-width: 1300px; width: 50%;"></div>
		<script>
			/*
			
				Based on "1.7 million points with async loading", at https://www.highcharts.com/stock/demo/lazy-loading
			
			*/
			
			// Load new data depending on the selected data range
			function reloadData(e) {
				var chart = Highcharts.charts[0];

				chart.showLoading('Reloading data...');
				$.getJSON('get-history-count.php?type=inb&start=' + Math.round(e.min) +
						'&end=' + Math.round(e.max) + '&callback=?', function (data) {

					chart.series[0].setData(data);
					chart.hideLoading();
				});
			}

			// Make JSONP requst to data handler
			$.getJSON('get-history-count.php?type=inb&callback=?', function (data) {
				
				// create chart
				Highcharts.stockChart('container-a', {
					chart: {
						type: 'spline',
						zoomType: 'x'
					},

					// add navigator to the top of the chart
					navigator: {
						adaptToUpdatedData: false,
						series: {
							data: data
						}
					},
					scrollbar: {
						liveRedraw: false
					},

					title: {
						text: 'Inbound (To City)'
					},
					
					credits: {
						enabled: true
					},
					
					exporting: {
						enabled: false
					},
					
					plotOptions: {
						series: {
							marker: {
								// disable markers
								enabled: false
							}
						}
					},

					rangeSelector: {
						buttons: [{
							type: 'hour',
							count: 1,
							text: '1h'
						}, {
							type: 'day',
							count: 1,
							text: '1d'
						}, {
							type: 'month',
							count: 1,
							text: '1m'
						}, {
							type: 'all',
							text: 'All'
						}],
						inputEnabled: true,
						selected: 3
					},

					xAxis: {
						events: {
							// reload data when range changes
							afterSetExtremes: reloadData
						},
						ordinal: false,
						type: 'datetime'
					},

					yAxis: {
						title: {
							text: 'Traffic Flow (cars/minute)'
						},
						floor: 0,
						opposite: false,
						labels: {
							align: 'left',
							y: -2,
							x: 2
						},
						min: 0
					},

					series: [{
						data: data,
						dataGrouping: {
							enabled: false
						},
						color: '#1a358c'
					}]
				});
			});
		</script>
	</head>
</html>