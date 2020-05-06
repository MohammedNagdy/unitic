// draw a line chart for sales
// get the data through ajax get requesst
var endPoint = "api/line-data"
$.ajax({
    method:"GET",
    url: endPoint,
    success: (data) => {
      labels = data.dates;
      defaultData = data.sales;
      // draw the chart from the data
      drawChart();
    },
    error: (data_error) => {
      console.log("error");
      console.log(data_error);
    }
});


//
// Sales chart
//

function drawChart(){
var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: labels,
        datasets: [{
            label: 'Daily Sales',
            backgroundColor: '' ,
            borderColor: '#FFF',
            data: defaultData
        }]
    },

    // Configuration options go here
    options: {
  legend: {
      labels: {
          fontColor: "white",
          fontSize: 12
      }
  },
  scales: {
      yAxes: [{
          ticks: {
              fontColor: "white",
              fontSize: 12,
              stepSize: 50,
              beginAtZero: true,
              // Include a dollar sign in the ticks
              callback: function(value, index, values) {
                  return '$' + value;
          }
        }
      }],
      xAxes: [{
          ticks: {
              fontColor: "white",
              fontSize: 12,
              stepSize: 1,
              beginAtZero: true
          }
      }]
    }
  }
})
};
