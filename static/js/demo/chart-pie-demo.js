// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

var total;
var ink;
var utg;
function loadJson(selector) {
  return JSON.parse(document.querySelector(selector).getAttribute('data-json'));
}

window.onload = function () {

  var jsonDataUt = loadJson('#jsonDataUt');
  var jsonDataIn = loadJson('#jsonDataIn');
  var totalUt=0;
  var totalIn=0;
  var dataUt = jsonDataUt.map((item) => item.amount);
  var dataIn = jsonDataIn.map((item) => item.amount);
  for (let index = 0; index < dataUt.length; index++) {
    totalUt = totalUt+dataUt[index];
    
  }
  for (let index = 0; index < dataIn.length; index++) {
    totalIn = totalIn+dataIn[index];
    
  }



// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ["Inkomst", "Utgift",],
    datasets: [{
      data: [totalUt, totalIn],
      backgroundColor: ['#4e73df', '#1cc88a'],
      hoverBackgroundColor: ['#2e59d9', '#17a673',],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});}
