var myChart = echarts.init(document.getElementById("balance-chart"));


option = {
  title: {
    text: "Balance History",
  },
  xAxis: {
    data: [],
  },
  yAxis: {},
  series: [
    {
      data: [],
      type: "line",
    },
  ],
  tooltip: {
    trigger: "axis",
  },
  grid: {
    top: "30px",
    // left: "px",
    right: "15px",
    bottom: "20px",
  },
};

myChart.setOption(option);

// get data from server
$.getJSON("/balance_history", function (data) {
  console.log(data);
  myChart.setOption({
    xAxis: {
      data: data.data.map(function (item) {
        return item[0];
      }),
    },
    series: [
      {
        data: data.data.map(function (item) {
          return item[1];
        }),
      },
    ],
  });
})