var hourlyChart = getTempChart();
var dailyChart = getTempChart();
var minsHourly = 60;
var minsDaily = 480;

function initChartsGauges() {
  updateGauges();
  renderCharts();
  nv.addGraph(hourlyChart);
  nv.addGraph(dailyChart);
}

function getTempChart() {
  var chart = nv.models.lineChart()
    .margin({left: 35})
    .useInteractiveGuideline(false)
    .transitionDuration(350)
    .showLegend(false)
    .showYAxis(true)
    .showXAxis(true);
  chart.xAxis
      //.axisLabel('Time')
      .tickFormat(function(d) { return d3.time.format('%H:%M')(new Date(d)); });
  chart.yAxis
      //.axisLabel('Temperature')
      .tickFormat(d3.format('.02f'));
  return chart;
}

function renderCharts() {
  // Hourly
  var startTime = (new Date() - (minsHourly * 60000)) / 1000;
  d3.json("/api?since=" + parseInt(startTime), function(error, json) {
    if (error) return console.warn(error);
    var tempData = processBraubuddyData(json);
    d3.select("#chart-hourly svg")
      .datum(tempData)
      .call(hourlyChart);
  });
  // Daily
  var startTime = (new Date() - (minsDaily * 60000)) / 1000;
  d3.json("/api?since=" + parseInt(startTime), function(error, json) {
    if (error) return console.warn(error);
    var tempData = processBraubuddyData(json);
    d3.select("#chart-daily svg")
      .datum(tempData)
      .call(hourlyChart);
  });
}

function updateGauges() {
  d3.json("/api?limit=1", function(error,json) {
    if (error) return console.warn(error);
    $('#temp-current').text(d3.format('.01f')(json[0][0]));
    $('#heat-level').text(json[0][1]);
    $('#cool-level').text(json[0][2]);
    $('#cycle-time').text(d3.time.format('%H:%M')(new Date(json[0][3] * 1000)));
  });
}

function processBraubuddyData(json) {
  var temp = [], heat = [], cool = [];
  for (var i=0;i<json.length;i++) {
    var timestamp = json[i][3]*1000;
    temp.push({x: timestamp, y: json[i][0]});
    heat.push({x: timestamp, y: json[i][1]});
    cool.push({x: timestamp, y: json[i][2]});
  }
  return [
    {
      values: temp,
      key: 'Temperature',
      color: '#ff7f0e'
    }
  ];
}
