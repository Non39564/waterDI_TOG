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
      dataP4.addRow([json[0].Data[0].id, json[0].Data[0].Water]);
      dataP4.addRow([json[0].Data[1].id, json[0].Data[1].Water]);
      dataP4.addRow([json[0].Data[2].id, json[0].Data[2].Water]);
      document.getElementById("Phase5").innerHTML = json[0].Station+" "+json[1].Phase;
      dataP5.addRow([json[1].Data[0].id, json[1].Data[0].Water]);
      dataP5.addRow([json[1].Data[1].id, json[1].Data[1].Water]);
      dataP5.addRow([json[1].Data[2].id, json[1].Data[2].Water]);
      dataP5.addRow([json[1].Data[3].id, json[1].Data[3].Water]);
      dataP5.addRow([json[1].Data[4].id, json[1].Data[4].Water]);
      document.getElementById("Phase9").innerHTML = json[0].Station+" "+json[2].Phase;
      dataP9.addRow([json[2].Data[0].id, json[2].Data[0].Water]);
      dataP9.addRow([json[2].Data[1].id, json[2].Data[1].Water]);
      dataP9.addRow([json[2].Data[2].id, json[2].Data[2].Water]);
      dataP9.addRow([json[2].Data[3].id, json[2].Data[3].Water]);
      dataP9.addRow([json[2].Data[4].id, json[2].Data[4].Water]);
      dataP9.addRow([json[2].Data[5].id, json[2].Data[5].Water]);

      chartP4.draw(dataP4, options);
      chartP5.draw(dataP5, options);
      chartP9.draw(dataP9, options);

      var toastLiveExample = document.getElementById('liveToast')
      for (i in json) {
        const d = new Date()
        const day = d.getDate()
        const month = d.getMonth()+1
        const year = d.getFullYear()
        const h = d.getHours()
        const m = d.getMinutes()
        if (m < 10) {
          const m = "0"+m
        }
        const erroralert = []
        for (j in json[i].Data) {
            if(json[i].Data[j].Water < 5) {
                var toast = new bootstrap.Toast(toastLiveExample);
                var macName = json[i].Data[j].id;
                erroralert.push(macName)
            }
        }
        if (erroralert.length > 0) {
          document.getElementById("AlertId").innerHTML = "Di Error<br> "+erroralert.join(" <br> ");
          document.getElementById("timealert").innerHTML = day+"/"+month+"/"+year+"          "+h+":"+m;
          toast.show()
        }
        
      }

    });
  }

  var chartP4 = new google.visualization.Gauge(document.getElementById('dataP4'));
  var chartP5 = new google.visualization.Gauge(document.getElementById('dataP5'));
  var chartP9 = new google.visualization.Gauge(document.getElementById('dataP9'));

  var options = {
    // width:1000, height:500,
    redFrom: 0, redTo: 5,
    yellowFrom: 5, yellowTo: 20,
    greenFrom: 20, greenTo: 30,
    min: 0, max: 30,
    minorTicks: 5
  };

    setInterval(drawGauge, 1000);
}

$(window).resize(function(){
  drawChart();
});
