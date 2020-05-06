// draw bar inventory chart

var endPoint = "api/line-data"
$.ajax({
		method:"GET",
		url: endPoint,
		success: (data) => {
			labels = data.dates;
			defaultData = data.inventory;
			// draw the chart from the data
			drawBar();
		},
		error: (data_error) => {
			console.log("error");
			console.log(data_error);
		}
});

//
// Bars chart
//

function drawBar() {

	//
	// Variables
	//



	//
	// Methods
	//

	// Init chart

		var $chart = $('#chartbars');

		// Create chart
		var ordersChart = new Chart($chart, {
			type: 'bar',
			data: {
				labels: labels,
				datasets: [{
					backgroundColor: 'orange',
					label: 'Inventory',
					data: defaultData
				}]
			},
			// Configuration options go here
			options: {
				responsive: true,
		legend: {
				labels: {
						fontColor: "black",
						fontSize: 12
				}
		},
		scales: {
				yAxes: [{
						ticks: {
								fontColor: "black",
								fontSize: 12,
								stepSize: 100,
								beginAtZero: true,
								// Include a dollar sign in the ticks
								callback: function(value, index, values) {
										return '$' + value;
						}
					}
				}],
				xAxes: [{
						ticks: {
								fontColor: "black",
								fontSize: 12,
								stepSize: 1,
								beginAtZero: true
						}
				}]
			}
		}
		});

		// Save to jQuery object
		$chart.data('chart', ordersChart);
	}
