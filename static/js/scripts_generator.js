window.Apex = {
    chart: {
      foreColor: "#fff",
      toolbar: {
        show: false,
      },
    },
    colors: ["#FCCF31", "#17ead9", "#f02fc2"],
    stroke: {
      width: 3,
    },
    dataLabels: {
      enabled: false,
    },
    grid: {
      borderColor: "#40475D",
    },
    xaxis: {
      axisTicks: {
        color: "#333",
      },
      axisBorder: {
        color: "#333",
      },
    },
    fill: {
      type: "gradient",
      gradient: {
        gradientToColors: ["#F55555", "#6078ea", "#6094ea"],
      },
    },
    tooltip: {
      theme: "dark",
      x: {
        formatter: function () {
          return moment(Date.now()).format("HH:mm:ss");
        },
      },
    },
    yaxis: {
      decimalsInFloat: 2,
      opposite: true,
      labels: {
        offsetX: -10,
      },
    },
  };
  
  var options = {
    series: [],
    chart: {
      height: 350,
      type: "line",
      stacked: true,
      animations: {
        enabled: true,
        easing: "linear",
        speed: 800,
        animateGradually: {
          enabled: true,
          delay: 150,
        },
        dynamicAnimation: {
          enabled: true,
          speed: 350,
        },
      },
      toolbar: {
        show: false,
      },
      zoom: {
        enabled: false,
      },
      dropShadow: {
        enabled: true,
        opacity: 0.3,
        blur: 5,
        left: -7,
        top: 22,
      },
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      curve: "smooth",
    },
    title: {
      text: "None data",
      align: "left",
    },
    xaxis: {
      categories: [],
    },
    noData: {
      text: "Loading...",
    },
  };
  
  var chart_line = new ApexCharts(
    document.querySelector("#line_Frequency"),
    options
  );
  chart_line.render();
  
  //################################################################################################
  var trigoStrength = 3
  var iteration = 11
  
  function generateMinuteWiseTimeSeries(baseval, count) {
    var i = 11;
    var series = [];
    while (i < count) {
      var x = baseval;
      var y = (0)
  
      series.push([x, y]);
      baseval += 1000;
      i++;
    }
    return series;
  }
  
  
  var optionsLine = {
    chart: {
      height: 350,
      type: 'line',
      stacked: true,
      animations: {
        enabled: true,
        easing: 'linear',
        dynamicAnimation: {
          speed: 1000
        }
      },
      dropShadow: {
        enabled: true,
        opacity: 0.3,
        blur: 5,
        left: -7,
        top: 22
      },
      events: {
        animationEnd: function (chartCtx, opts) {
          const newData1 = chartCtx.w.config.series[0].data.slice()
          newData1.shift()
  
          // check animation end event for just 1 series to avoid multiple updates
          if (opts.el.node.getAttribute('index') === '0') {
            window.setTimeout(function () {
              chartCtx.updateOptions({
                series: [{
                  data: newData1
                }],
              }, false)
            }, 300)
          }
  
        }
      },
      toolbar: {
        show: false
      },
      zoom: {
        enabled: false
      }
    },
    dataLabels: {
      enabled: false
    },
    stroke: {
      curve: 'smooth',
      width: 5,
    },
    grid: {
      padding: {
        left: 0,
        right: 0
      }
    },
    markers: {
      size: 0,
      hover: {
        size: 0
      }
    },
    series: [{
      name: "Frequency",
      data: generateMinuteWiseTimeSeries(new Date().getTime(), 12)
    }],
    xaxis: {
        labels: {
            show: false
          },
        type: 'datetime',
        range: 30000
    }
  }
  
  var chartLine = new ApexCharts(
    document.querySelector("#linechart"),
    optionsLine
  );
  chartLine.render()
  //################################################################################################
  var datause = [];
  var time = [];
  window.setInterval(function () {
    $.getJSON("/dataapi_generator").done(function (json) {
      for (i in json) {
        datause.push(json[i].Frequency);
        time.push(json[i].Time);
        if (datause.length == 11) {
          datause.shift();
          time.shift();
        }
        //######################################################################
        iteration++;
        chartLine.updateSeries([{
          data: [...chartLine.w.config.series[0].data,
            [
              chartLine.w.globals.maxX + 1000,
              datause[datause.length - 1]
  
            ]
          ]
        }])
        //######################################################################
      }
      $( "#freence" ).text("Frequency is " + json[0]["Frequency"] + " Hz");
      $( "#temp" ).text("Coolant Temp is " + json[0]["Coolant Temp"] + " C");
 
      if (json[0].Mode === "Auto"){
        $('#Mode_Switch').text("Auto");
        $('#Mode_Switch').addClass("text-success");
      } else if (json[0].Mode === "Manual"){
        $('#Mode_Switch').text("Manual");
        $('#Mode_Switch').addClass("text-warning");
      } else if (json[0].Mode === "Off") {
        $('#Mode_Switch').text("OFF");
        $('#Mode_Switch').addClass("text-danger");
      }
  
      $("#L1Kw").text(json[0]["Power (A)"][0].L1+ ' A');
      $("#L2Kw").text(json[0]["Power (A)"][0].L2+ ' A');
      $("#L3Kw").text(json[0]["Power (A)"][0].L3+ ' A');
      $("#total-Kw").text(json[0]["Power (A)"][0].Total+ ' A');
  
      $("#L1V").text(json[0]["Power (V)"][0].L1+ ' V');
      $("#L2V").text(json[0]["Power (V)"][0].L2+ ' V');
      $("#L3V").text(json[0]["Power (V)"][0].L3+ ' V');
      $("#total-V").text(json[0]["Power (V)"][0].Total+ ' V');
  
      if (json[0].Status === "Off"){
        $('#Status').text("Off");
        $('#Status').css("color","#fa0000");
      } else if (json[0].Status === "Stop"){
        $('#Status').text("Stop");
        $('#Status').css("color","#ff983d");
      } else if (json[0].Status === "Preheat") {
        $('#Status').text("Preheat");
        $('#Status').css("color","#faed7d");
      } else if (json[0].Status === "Precrank") {
        $('#Status').text("Precrank");
        $('#Status').css("color","#e0d5d5");
      } else if (json[0].Status === "Crank") {
        $('#Status').text("Crank");
        $('#Status').css("color","#f0c0c0");
      } else if (json[0].Status === "Starter Disconnect") {
        $('#Status').text("Starter Disconnect");
        $('#Status').css("color","#f55bb2");
      } else if (json[0].Status === "PreRamp") {
        $('#Status').text("PreRamp");
        $('#Status').css("color","#8276f5");
      } else if (json[0].Status === "Running") {
        $('#Status').text("Running");
        $('#Status').css("color","#05f535");
      } else if (json[0].Status === "Fault Shutdown") {
        $('#Status').text("Fault Shutdown");
        $('#Status').css("color","#a505f5");
      } else if (json[0].Status === "Prerun Setup") {
        $('#Status').text("Prerun Setup");
        $('#Status').css("color","#00ebf7");
      } else if (json[0].Status === "Runtime Setup") {
        $('#Status').text("Runtime Setup");
        $('#Status').css("color","#00f7be");
      } else if (json[0].Status === "Ramp") {
        $('#Status').text("Ramp");
        $('#Status').css("color","#2505f5");
      } else if (json[0].Status === "Factory Setup") {
        $('#Status').text("Factory Setup");
        $('#Status').css("color","#d2f700");
      } else if (json[0].Status === "Waiting For Powerdown") {
        $('#Status').text("Waiting For Powerdown");
        $('#Status').css("color","#ff6a00");
      }
    });
    
  }, 1000);
  