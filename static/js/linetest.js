google.charts.load('current', {'packages':['line']});
google.charts.setOnLoadCallback(drawChart);

var timer = [];
var dataone = [];
var datatwo = [];
var datathree = [];

function drawChart() {

    var options = {
        chart: {
          title: 'Box Office Earnings in First Two Weeks of Opening',
          subtitle: 'in millions of dollars (USD)'
        },
        width: 900,
        height: 500
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
        dataone.push(json[2].Data[2].Water);
        datatwo.push(json[2].Data[1].Water);
        datathree.push(json[1].Data[1].Water);
         if (timer.length == 11) {
            timer.shift();
            dataone.shift();
            datatwo.shift();
            datathree.shift();
         };

        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Time');
        data.addColumn('number', 'Data1');
        data.addColumn('number', 'Data2');
        data.addColumn('number', 'Data3');
        for(i = 0; i < timer.length; i++){
            data.addRow([timer[i], dataone[i], datatwo[i], datathree[i]]);
        };
        // data.addRow([timer, dataone, datatwo, datathree]);
        
        console.log("data1 = "+dataone)
        console.log("data2 = "+datatwo)
        console.log("data3 = "+datathree)
        console.log("time = "+timer)
        
        chart.draw(data, google.charts.Line.convertOptions(options));
        }); 
    }
    setInterval(drawLine, 2000);

var chart = new google.charts.Line(document.getElementById('linechart_material'));
}