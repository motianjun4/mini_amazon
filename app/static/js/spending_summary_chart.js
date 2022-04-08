var spending_chart = echarts.init(document.getElementById("spending-summary-chart"));


option = {
  title: {
    text: "Spending",
  },
  xAxis: {
    type: "time",
  },
  yAxis: {},
  series: [
    {
      data: [],
      type: "bar",
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

spending_chart.setOption(option);

// get data from server
$.getJSON("/spending_summary", function (data) {
  console.log(data);
  spending_chart.setOption({
    series: [
      {
        data: data.data,
      },
    ],
  });
})