google.charts.load('current', {'packages':['line']});
google.charts.setOnLoadCallback(drawLineChart);

var timer = [];


$.getJSON('/dataapi', function (json) {
  //P4
  for (i in json ){
    window[json[0].Data[i].id.replace(/ +/g, "")] = [];
  }
  //P5
  for (i in json[1].Data ){
    window[json[1].Data[i].id.replace(/ +/g, "")] = [];
  }
  //P9
  for (i in json[2].Data ){
    window[json[2].Data[i].id.replace(/ +/g, "").replace(/-/g, "")] = [];
  }
})

function drawLineChart() {

    var optionsLP4 = {
        chart: {
          title: 'Phase4',
        },
      //   width: 500,
      // height: 250
    };

    var optionsLP5 = {
      chart: {
        title: 'Phase5',
      },
      // width: 500,
      // height: 250
    };

    var optionsLP9 = {
      chart: {
        title: 'Phase9',
      },
      // width: 500,
      // height: auto
    };

      function drawLine() {
        $.getJSON('/dataapi', function (json) {
        function addLeadingZero(num) {
            return (num <= 9) ? ("0" + num) : num;
          }
    
        currDate = new Date(),
        time = addLeadingZero(currDate.getHours()) + ":" +
        addLeadingZero(currDate.getMinutes()) + ":" +
        addLeadingZero(currDate.getSeconds());
        
        timer.push(time.toString());
        //P4
        for (i in json){
          window[json[0].Data[i].id.replace(/ +/g, "")].push(json[0].Data[i].Water);
        }
        //P5
        for (i in json[1].Data){
          window[json[1].Data[i].id.replace(/ +/g, "")].push(json[1].Data[i].Water);
          console.log()
        }
        //P9
        for (i in json[2].Data){
          window[json[2].Data[i].id.replace(/ +/g, "").replace(/-/g, '')].push(json[2].Data[i].Water);
        }
        if (timer.length == 11) {
           timer.shift();
           //P4
           for (i in json ){
             window[json[0].Data[i].id.replace(/ +/g, "")].shift();
           }
           //P5
           for (i in json[1].Data ){
             window[json[1].Data[i].id.replace(/ +/g, "")].shift();
           }
           //P9
           for (i in json[2].Data ){
             window[json[2].Data[i].id.replace(/ +/g, "").replace(/-/g, '')].shift();
           }
        };

        var dataLP4 = new google.visualization.DataTable();

        dataLP4.addColumn('string', 'Time');
        for (i in json){
          dataLP4.addColumn('number', json[0].Data[i].id);
        }
          for (i = 0; i < timer.length; i++){
          dataLP4.addRow([timer[i], ROBOT[i], Fisa2[i], Fisa4[i]]);
        };
        
        var dataLP5 = new google.visualization.DataTable();
        dataLP5.addColumn('string', 'Time');
        for (i in json[1].Data){
          dataLP5.addColumn('number', json[1].Data[i].id);
        }
        for(i = 0; i < timer.length; i++){
          dataLP5.addRow([timer[i], L15Station1[i], L15Station2[i], Fisa3[i], L13[i], L14[i]]);
        };

        var dataLP9 = new google.visualization.DataTable();
        dataLP9.addColumn('string', 'Time');
        for (i in json[2].Data){
          dataLP9.addColumn('number', json[2].Data[i].id);
        }
        for(i = 0; i < timer.length; i++){
          dataLP9.addRow([timer[i], HC4[i], HC5Station1[i], HC5Station2[i], AI[i], HC3[i], HC6[i]]);
        };

        chartLP4.draw(dataLP4, google.charts.Line.convertOptions(optionsLP4));
        chartLP5.draw(dataLP5, google.charts.Line.convertOptions(optionsLP5));
        chartLP9.draw(dataLP9, google.charts.Line.convertOptions(optionsLP9));
        }); 
    }
    //setInterval(drawLine, 1000);

var chartLP4 = new google.charts.Line(document.getElementById('linechartP4'));
var chartLP5 = new google.charts.Line(document.getElementById('linechartP5'));
var chartLP9 = new google.charts.Line(document.getElementById('linechartP9'));
}

$(window).resize(function(){
  drawLineChart();
});