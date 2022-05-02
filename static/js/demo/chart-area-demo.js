// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

function number_format(number, decimals, dec_point, thousands_sep) {
  // *     example: number_format(1234.56, 2, ',', ' ');
  // *     return: '1 234,56'
  number = (number + '').replace(',', '').replace(' ', '');
  var n = !isFinite(+number) ? 0 : +number,
    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
    sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
    dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
    s = '',
    toFixedFix = function(n, prec) {
      var k = Math.pow(10, prec);
      return '' + Math.round(n * k) / k;
    };
  // Fix for IE parseFloat(0.55).toFixed(0) = 0;
  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || '').length < prec) {
    s[1] = s[1] || '';
    s[1] += new Array(prec - s[1].length + 1).join('0');
  }
  return s.join(dec);
}

function loadJson(selector) {
  return JSON.parse(document.querySelector(selector).getAttribute('data-json'));
}

var jsonDataUt = loadJson('#jsonDataUt');
var jsonDataIn = loadJson('#jsonDataIn');

var totalUt=0;
var totalIn=0;
var dataUt = jsonDataUt.map((item) => item.amount);
var dataIn = jsonDataIn.map((item) => item.amount);
console.log(dataIn)
// creating the seven days based on the current ca
var date = jsonDataIn.map((item) => item.date);
days=['Monday','Tuesday','Wednesday', 'Thursday', 'Friday','Saturday','Sunday']
orderedDays=[]
for (let day = 0; day < 7; day++) {
  if (date==days[day]){
    orderedDays[0]=date[0];
    for (let startDay = 1; startDay < 7; startDay++) {
      if(day+startDay<7){
        orderedDays[startDay] = days[day+startDay];
      }
      else if( day+startDay>6){
          for (let Beg = 0; Beg < day; Beg++) {
            orderedDays[startDay+Beg]=days[Beg]
          }
      if (orderedDays.length=7){
        break;
      }
      }
    }
  }
}
orderedDays[7]=orderedDays[0]
orderedDays.splice(0,1)
labels=orderedDays
console.log(orderedDays)
for (let index = 0; index < dataUt.length; index++) {
  totalUt = totalUt+dataUt[index];
  
}
for (let index = 0; index < dataIn.length; index++) {
  totalIn = totalIn+dataIn[index];
  
}
//end of week names

//start of totalUtgifter inom en vecka
var jsonWeek=loadJson('#veckoutdata');
var weekUt = jsonWeek.map((item) => item.totalUtgift);

console.log(weekUt);
//end of  totalUtgifter inom en vecka
var jsonWeek=loadJson('#veckoutdata');
var weekIn = jsonWeek.map((item) => item.totalInkomst);

//start of totalInkomster of the week


// Area Chart Example
var ctx = document.getElementById("myAreaChart");
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: orderedDays,
    datasets: [{
      label: "inkomster",
      lineTension: 0.3,
      backgroundColor: "rgba(28,200,138,0.05)",
      borderColor: "rgba(28,200,138)",
      pointRadius: 3,
      pointBackgroundColor: "rgba(28,200,138)",
      pointBorderColor: "rgba(28,200,138)",
      pointHoverRadius: 3,
      pointHoverBackgroundColor: "rgba(28,200,138)",
      pointHoverBorderColor: "rgba(28,200,138)",
      pointHitRadius: 10,
      pointBorderWidth: 2,
      data: weekIn,
    },{
      label: "Utgifter",
      lineTension: 0.3,
      backgroundColor: "rgba(78, 115, 223, 0.05)",
      borderColor: "rgba(78, 115, 223, 1)",
      pointRadius: 3,
      pointBackgroundColor: "rgba(78, 115, 223, 1)",
      pointBorderColor: "rgba(78, 115, 223, 1)",
      pointHoverRadius: 3,
      pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
      pointHoverBorderColor: "rgba(78, 115, 223, 1)",
      pointHitRadius: 10,
      pointBorderWidth: 2,
      data: weekUt,
    },
  
  
  ],
  },
  options: {
    maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 25,
        bottom: 0
      }
    },
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
        },
        gridLines: {
          display: false,
          drawBorder: false
        },
        ticks: {
          maxTicksLimit: 7
        }
      }],
      yAxes: [{
        ticks: {
          maxTicksLimit: 5,
          padding: 10,
          // Include a dollar sign in the ticks
          callback: function(value, index, values) {
            return '$' + number_format(value);
          }
        },
        gridLines: {
          color: "rgb(234, 236, 244)",
          zeroLineColor: "rgb(234, 236, 244)",
          drawBorder: false,
          borderDash: [2],
          zeroLineBorderDash: [2]
        }
      }],
    },
    legend: {
      display: false
    },
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      titleMarginBottom: 10,
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      intersect: false,
      mode: 'index',
      caretPadding: 10,
      callbacks: {
        label: function(tooltipItem, chart) {
          var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
          return datasetLabel + ': $' + number_format(tooltipItem.yLabel);
        }
      }
    }
  }
});

