nv.addGraph(function() {
  var data_mins = 60
  var chart = nv.models.lineChart()
                .margin({left: 35})  //Adjust chart margins to give the x-axis some breathing room.
                .useInteractiveGuideline(true)  //We want nice looking tooltips and a guideline!
                .transitionDuration(350)  //how fast do you want the lines to transition?
                .showLegend(false)       //Show the legend, allowing users to turn on/off line series.
                .showYAxis(true)        //Show the y-axis
                .showXAxis(true)        //Show the x-axis
  ;

  chart.xAxis     //Chart x-axis settings
      //.axisLabel('Time')
      .tickFormat(function(d) { return d3.time.format('%H:%M')(new Date(d)); })

  chart.yAxis     //Chart y-axis settings
      //.axisLabel('Temperature')
      .tickFormat(d3.format('.02f'));

  //Get data points for past hour
  var startTime = (new Date() - (data_mins * 60000)) / 1000 
  d3.json("/api/status?since=" + parseInt(startTime), function(error, json) {
    if (error) return console.warn(error);
    var myData = processBbJson(json)
    d3.select('#chart-hourly svg')    //Select the <svg> element you want to render the chart in.   
      .datum(myData)         //Populate the <svg> element with chart data...
      .call(chart);          //Finally, render the chart!
  });

  //Update the chart when window resizes.
  nv.utils.windowResize(function() { chart.update() });
  return chart;
});

nv.addGraph(function() {
  var data_mins = 480
  var chart = nv.models.lineChart()
                .margin({left: 35})  //Adjust chart margins to give the x-axis some breathing room.
                .useInteractiveGuideline(true)  //We want nice looking tooltips and a guideline!
                .transitionDuration(350)  //how fast do you want the lines to transition?
                .showLegend(false)       //Show the legend, allowing users to turn on/off line series.
                .showYAxis(true)        //Show the y-axis
                .showXAxis(true)        //Show the x-axis
  ;

  chart.xAxis     //Chart x-axis settings
      //.axisLabel('Time')
      .tickFormat(function(d) { return d3.time.format('%H:%M')(new Date(d)); })

  chart.yAxis     //Chart y-axis settings
      //.axisLabel('Temperature')
      .tickFormat(d3.format('.02f'));

  //Get data points for past hour
  var startTime = (new Date() - (data_mins * 60000)) / 1000 
  d3.json("/api/status?since=" + parseInt(startTime), function(error, json) {
    if (error) return console.warn(error);
    var myData = processBbJson(json)
    d3.select('#chart-daily svg')    //Select the <svg> element you want to render the chart in.   
      .datum(myData)         //Populate the <svg> element with chart data...
      .call(chart);          //Finally, render the chart!
  });

  //Update the chart when window resizes.
  nv.utils.windowResize(function() { chart.update() });
  return chart;
});

function processBbJson(json) {
  var temp = [], heat = [], cool = [];
  for (var i=0;i<json.length;i++) {
    var timestamp = json[i][3]*1000
    temp.push({x: timestamp, y: json[i][0]})
    heat.push({x: timestamp, y: json[i][1]})
    cool.push({x: timestamp, y: json[i][2]})
  }
  return [
    {
      values: temp,
      key: 'Temperature',
      color: '#ff7f0e'
    }
  ];
}
