var purchase_category_chart = echarts.init(document.getElementById("fulfill-chart"));


option = {
  title: {
    text: "Seller Fulfill Rate",
  },
  tooltip: {
    trigger: "item",
  },
  legend: {
    y: "bottom",
  },
  series: [
    {
      name: "Fulfill Status",
      type: "pie",
      radius: ["40%", "70%"],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: "#fff",
        borderWidth: 2,
      },
      label: {
        show: false,
        position: "center",
      },
      data: [],
    },
  ],
};

purchase_category_chart.setOption(option);

// get data from server
$.getJSON("/sell_fulfill", function (data) {
  let new_data = data.data.map((item)=>{
          return {
            name: item.name,
            value: item.count,
          }
        })
  console.log(new_data)
  purchase_category_chart.setOption({
    series: [
      {
        name: "Status",
        data: new_data,
      },
    ],
  });
});