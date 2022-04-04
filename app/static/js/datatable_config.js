// Use with ajax_table.html
// Store configuration separately in this file
window.datatable_config = {
  "sell-table": [
    {
      title: "Product",
      data: "product",
      render: (data, type, row) => {
        console.log(data);
        return `<img style="width:3em; height: 3em; margin-right: 1em" src="/img/product_${data.id}.jpg" /><a href="/product/${data.id}">${data.name}</a>`;
      },
    },
    { title: "Price", data: "price" },
  ],
  "recent-purchase": [
    {
      title: "ID",
      data: "id",
    },
    {
      title: "Product",
      data: "product",
      render: (data, type, row) => {
        return `<img style="width:3em; height: 3em; margin-right: 1em" src="/img/product_${data.pid}.jpg" /><a href="/product/${data.pid}">${data.name}</a>`;
      },
    },
    {
        title:"Order",
        data:"order",
        render:(data,type,row)=>{
            return `<a href="/order/${data.oid}">${data.buydate}</a>`;
        }
    },
    {
        title:"Price",
        data:"price"
    },
    {
        title:"Quantity",
        data:"count"
    }
  ],
};