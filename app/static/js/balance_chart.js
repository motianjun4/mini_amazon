var balance_chart = echarts.init(document.getElementById("balance-chart"));


option = {
  title: {
    text: "Balance History",
  },
  xAxis: {
    type: "time",
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
    left: "60px",
    right: "15px",
    bottom: "20px",
  },
};

balance_chart.setOption(option);

// get data from server
$.getJSON("/balance_history", function (data) {
  console.log(data);
  balance_chart.setOption({
    series: [
      {
        data: data.data,
      },
    ],
  });
})