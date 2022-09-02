google.charts.load('current', {'packages':['gauge']});
google.charts.setOnLoadCallback(drawChart);

var start = new Date().getTime();
var end = new Date().getTime();
var time = end - start;

function drawChart() {

  function drawGauge() {
    $.getJSON('/dataapi').done(function (json){

      var dataP4 = new google.visualization.DataTable();
      dataP4.addColumn('string', 'Label');
      dataP4.addColumn('number', 'Value');

      var dataP5 = new google.visualization.DataTable();
      dataP5.addColumn('string', 'Label');
      dataP5.addColumn('number', 'Value');

      var dataP9 = new google.visualization.DataTable();
      dataP9.addColumn('string', 'Label');
      dataP9.addColumn('number', 'Value');

      document.getElementById("Phase4").innerHTML = json[0].Station+" "+json[0].Phase;
      for (i in json[0].Data) {
        dataP4.addRow([json[0].Data[i].id, json[0].Data[i].Water])
      }
 

      document.getElementById("Phase5").innerHTML = json[0].Station+" "+json[1].Phase;
      for (i in json[1].Data) {
        dataP5.addRow([json[1].Data[i].id, json[1].Data[i].Water]);
      }


      document.getElementById("Phase9").innerHTML = json[0].Station+" "+json[2].Phase;
      for (i in json[2].Data) {
        dataP9.addRow([json[2].Data[i].id, json[2].Data[i].Water]);
      }

          
      chartP4.draw(dataP4, options);
      chartP5.draw(dataP5, options);
      chartP9.draw(dataP9, options);

    });
  }

  var chartP4 = new google.visualization.Gauge(document.getElementById('dataP4'));
  var chartP5 = new google.visualization.Gauge(document.getElementById('dataP5'));
  var chartP9 = new google.visualization.Gauge(document.getElementById('dataP9'));

  var options = {
    redFrom: 0, redTo: 10, redColor: "FF3838" ,
    yellowFrom: 20, yellowTo: 30, yellowColor: "FF3838",
    greenFrom: 10, greenTo: 20,greenColor: "16F200",
    min: 0, max: 30,
    minorTicks: 0,
    
  };

  setInterval(drawGauge, 1000);
}

$(window).resize(function(){
  drawChart();
});
