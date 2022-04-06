// Use with datatable.html
// Store configuration separately in this file
window.datatable_config = {
  "cart-list": [
    {
      title: "ID",
      data: "cid",
    },
    {
      title: "Product",
      data: "product",
      render: (data, type, row) => {
        return `<img style="width:3em; height: 3em; margin-right: 1em" src="/img/product_${data.pid}.jpg" /><a href="/product/${data.pid}">${data.name}</a>`;
      },
    },
    {
      title: "Sold By",
      data: "seller",
      render: (data, type, row) => {
        return `<a href="/user/${data.id}">${data.name}</a>`;
      },
    },
    {
      title: "Price",
      data: "price",
    },
    {
      title: "Quantity",
      data: "quantity",
    },
    {
      title: "Total",
      data: "total",
    },
    {
      title: "Action",
      data: "cid",

      render: (data, type, row) => {
        return `<button class="btn btn-danger" onclick="remove_cart_item(${data})">Remove</button>`;
      },
    },
  ],
  "product-search-list": [
    {
      title: "Name",
      data: "name",
    },
    {
      title: "Price",
      data: "price",
    },
  ],
  "sell-table": [
    {
      title: "Product",
      data: "product",
      render: (data, type, row) => {
        return `<img style="width:3em; height: 3em; margin-right: 1em" src="/img/product_${data.id}.jpg" /><a href="/product/${data.id}">${data.name}</a>`;
      },
    },
    { title: "Price", data: "price" },
  ],
  "seller-table": [
    {
      title: "Seller",
      data: "seller",
      render: (data, type, row) => {
        return `<a href="/user/${data.id}">${data.name}</a>`;
      },
    },
    { title: "Price", data: "price" },
    { title: "Quantity", data: "quantity" },
    {
      title: "Action",
      data: "iid",
      orderable: false,
      width: "17em",
      render: (data, type, row) => {
        return `
      <form class="form-inline my-2 my-lg-0 mr-2">
        <input id="key_${data}_quantity" type="number" class="form-control form-inline mr-1" min="1" style="width: 7em;" placeholder="Quantity">
        <a id="key_${data}_add_cart" class="btn btn-primary" style="width: 7em;" href="javascript:add_cart_button_onclick(${data}, ${data})">Add to cart</button>
      </form>
      
      `;
      },
    },
  ],
  "recent-purchase": [
    {
      title: "Product",
      data: "product",
      render: (data, type, row) => {
        return `<img style="width:3em; height: 3em; margin-right: 1em" src="/img/product_${data.pid}.jpg" /><a href="/product/${data.pid}">${data.name}</a>`;
      },
    },
    {
      title: "Order",
      data: "oid",
      render: (data, type, row) => {
        if (type != "display") {
          return data;
        }
        return `<a href="/order/${data}">#${data}</a>`;
      },
    },
    {
      title: "Purchase At",
      data: "purchase_time",
      render: (data, type, row) => {
        if (type != "display") {
          return data;
        }
        return `${format_time(data)}`;
      },
    },
    {
      title: "Price",
      data: "price",
    },
    {
      title: "Quantity",
      data: "count",
    },
    {
      title: "Total",
      data: "total",
    },
    {
      title:"Fulfillment",
      data: "fulfillment",
      render: (data, type, row) => {
        if (data === true) {
          return `<span class="badge badge-success">Fulfilled</span>`;
        } else {
          return `<span class="badge badge-warning">Pending</span>`;
        }
      }
    }
  ],
  "order-purchase": [
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
      title: "Seller",
      data: "seller",
      render: (data, type, row) => {
        if(type!="display"){
          return data.name;
        }
        return `<a href="/user/${data.uid}">${data.name}</a>`;
      }
    },
    {
      title: "Price",
      data: "price",
    },
    {
      title: "Quantity",
      data: "count",
    },
    {
      title: "Fulfillment",
      data: "fulfillment",
    },
    {
      title: "Review",
      data: "sid",
      render: (data, type, row) => {
        return `<a class="btn btn-primary" href="/user/${data}#my_review">View</a>`;
      },
    },
  ],
  "my-inventory": [
    {
      title: "Product",
      data: "product",
      render: (data, type, row) => {
        return `<img style="width:3em; height: 3em; margin-right: 1em" src="/img/product_${data.id}.jpg" /><a href="/product/${data.id}">${data.name}</a>`;
      },
    },
    { title: "Price", data: "price" },
    { title: "Quantity", data: "quantity" },
    {
      title: "Action",
      data: "iid",
      orderable: false,
      width: "4em",
      render: (data, type, row) => {
        return `<a class="btn btn-primary" href="/inventory/${data}">Edit</a> <a class="btn btn-danger" href="/deleteInventory/${data}">Delete</a>`;
      },
    },
  ],
  "product-detail-review": [
    { title: "Create Date", data: "create_at" },
    { title: "User", data: "creator" },
    { title: "Review", data: "review" },
    { title: "Rates", data: "rate" },
    { title: "Upvotes", data: "upvote_cnt" },
  ],
  "public-user-review": [
    { title: "Create Date", data: "create_at" },
    { title: "User", data: "creator" },
    { title: "Review", data: "review" },
    { title: "Rates", data: "rate" },
    { title: "Upvotes", data: "upvote_cnt" },
  ],
  "order-fulfill": [
    {
      title: "ID",
      data: "oid",
      render: (data, type, row) => {
        if (type === "display") {
        return `<a href="/order/${data}">#${data}</a>`;
        }
        return data;
      },
    },
    {
      title: "Product",
      data: "product",
      render: (data, type, row) => {
        return `<a href="/product/${data.pid}">${data.name}</a>`;
      },
    },
    {
      title: "Buyer",
      data: "buyer",
      render: (data, type, row) => {
        return `<a href="/user/${data.id}">${data.name}</a>`;
      },
    },
    { title: "Address", data: "address" },
    {
      title: "Tel",
      data: "tel",
      render: (data, type, row) => {
        return `<a href="tel:${data}">${data}</a>`;
      },
    },
    { title: "Create At", data: "create_at" },
    // {title:"Categories", data:"categories"},
    { title: "Quantity", data: "total_amount" },
    {
      title: "Fulfillment",
      data: "fulfillment",
      render: (data, type, row) => {
        console.log(row);
        return data
          ? `<a class="btn btn-light btn-sm" style="width:6em" disabled>Confirmed</a>`
          : `<button class="btn btn-success btn-sm" style="width:6em" onclick="confirm_purchase_fulfillment(${row.purchase_id})">Confirm</button>`;
      },
    },
  ],
  "reviews-for-product": [
    { title: "Time", data: "time" },
    {
      title: "Product",
      data: "product",
      render: (data, type, row) => {
        return `<img style="width:3em; height: 3em; margin-right: 1em" src="/img/product_${data.id}.jpg" /><a href="/product/${data.id}">${data.name}</a>`;
      },
    },
    { title: "Review", data: "review" },
    {
      title: "Rate",
      data: "rate",
      width: "5em",
      render: (data, type, row) => {
        return (
          `<i class="bi bi-star-fill"></i>`.repeat(data) +
          `<i class="bi bi-star"></i>`.repeat(5 - data)
        );
      },
    },
    {
      title: "Action",
      data: "product",
      render: (data, type, row) => {
        return `<div><a href="/review/product/edit?pid=${data.id}&redirect=user">Edit</a></div><div> <a href="/review/product/remove?pid=${data.id}&redirect=user">Remove</a></div>`;
      },
    },
  ],
  "reviews-for-seller": [
    { title: "Time", data: "time" },
    {
      title: "Seller",
      data: "seller",
      render: (data, type, row) => {
        return `<a href="/user/${data.id}">${data.name}</a>`;
      },
    },
    { title: "Review", data: "review" },
    {
      title: "Rate",
      data: "rate",
      width: "5em",
      render: (data, type, row) => {
        return (
          `<i class="bi bi-star-fill"></i>`.repeat(data) +
          `<i class="bi bi-star"></i>`.repeat(5 - data)
        );
      },
    },
    {
      title: "Action",
      data: "seller",
      render: (data, type, row) => {
        return `<div><a href="/review/seller/edit?sid=${data.id}&redirect=user">Edit</a></div><div> <a href="/review/seller/remove?sid=${data.id}&redirect=user">Remove</a></div>`;
      },
    },
  ],
};

window.datatable_created_row = {
  "product-search-list": (row, item, index) =>{
    row.innerHTML = ""

    html = `
      <td colspan="2">
      <div class="card">
        <div class="card-body" style="display:flex">
            <div>
                <img src="/img/product_${item.id}.jpg" style="height: 5em; width:5em;">
            </div>
            
            <div class="ml-2" style="flex-grow:1">
                <h4 class="card-title"><a href="/product/${item.id}">${item.name}</a></h4>
                <p class="card-text">Starting from: $${item.price}</p>
            </div>
            <div>
                <input id="key_${item.id}_quantity" type="number" class="form-control mb-2" min="1" style="width: 7em;" placeholder="Quantity">
                <a id="key_${item.id}_add_cart" class="btn btn-primary" href="javascript:add_cart_button_onclick(${item.id}, ${item.iid})" style="width: 7em;">Add to cart</a>
            </div>
        </div>        
      </div>

      </td>
    `;
    row.innerHTML = html
  },
  "public-user-review": (row, review, index) => {
    row.innerHTML=""
    html = `
      <td colspan="5">
      <div class="card text-left">
                <div class="card-body">
                  <div class="row">
                    <div class="col">
                      <h4 class="card-title"><span class="text-secondary" style="font-size:0.7em">#${
                        review.id
                      } </span><a href="/user/${review.uid}">${
      review.creator
    }</a>
                      ${
                        window.current_user_id == review.uid
                          ? `<span class="text-secondary" style="font-size: 0.7em;">(You)</span>`
                          : ""
                      }
                      </h4>
                    </div>
                    <div class="col" style="text-align: right;">
                    ${
                      `<i class="bi bi-star-fill"></i>`.repeat(review.rate) +
                      `<i class="bi bi-star"></i>`.repeat(5 - review.rate)
                    }
                      <button type="button" class="btn ${
                        review.is_upvote ? "btn-dark" : "btn-light"
                      }" 
                        onclick="upvote_review(${review.id}, ${
      review.is_upvote
    })">
                        <i class="bi bi-hand-thumbs-up"></i>${
                          review.upvote_cnt
                        }</button>
                      <button type="button" class="btn ${
                        review.is_downvote ? "btn-dark" : "btn-light"
                      } mr-2"
                        onclick="downvote_review(${review.id}, ${
      review.is_downvote
    })">
                        <i class="bi bi-hand-thumbs-down"></i>${
                          review.downvote_cnt
                        }</button>
                      
                    </div>
                  </div>
                  <p class="card-text">${review.review}</p>
                  <div class="text-right">
                      ${
                        //new Date(review.create_at).toDateString()+" "+new Date(review.create_at).toLocaleTimeString()
                        format_time(review.create_at)
                      }
                  </div>
                </div>
              </div>
      </td>
      `;
      row.innerHTML = html
  },
  "product-detail-review": (row, review, index) => {
    row.innerHTML=""
    html = `
      <td colspan="5">
      <div class="card text-left">
                <div class="card-body">
                  <div class="row">
                    <div class="col">
                      <h4 class="card-title">
                      <span class="text-secondary" style="font-size:0.7em">#${
                        review.id
                      } </span>
                      <a href="/user/${review.uid}">${review.creator}</a>
                      ${
                        window.current_user_id == review.uid
                          ? `<span class="text-secondary" style="font-size: 0.7em;">(You)</span>`
                          : ""
                      }
                      </h4>
                    </div>
                    <div class="col" style="text-align: right;">
                    ${
                      `<i class="bi bi-star-fill"></i>`.repeat(review.rate) +
                      `<i class="bi bi-star"></i>`.repeat(5 - review.rate)
                    }
                      <button type="button" class="btn ${
                        review.is_upvote ? "btn-dark" : "btn-light"
                      }" 
                        onclick="upvote_review(${review.id}, ${
      review.is_upvote
    })">
                        <i class="bi bi-hand-thumbs-up"></i>${
                          review.upvote_cnt
                        }</button>
                      <button type="button" class="btn ${review.is_downvote?"btn-dark":"btn-light"} mr-2"
                        onclick="downvote_review(${review.id}, ${review.is_downvote})">
                        <i class="bi bi-hand-thumbs-down"></i>${
                        review.downvote_cnt
                      }</button>
                      
                    </div>
                  </div>
                  <p class="card-text">${review.review}</p>
                  <div class="text-right">
                      ${
                        // new Date(review.create_at).toDateString() +
                        // " " +
                        // new Date(review.create_at).toLocaleTimeString()
                        format_time(review.create_at)
                      }
                  </div>
                </div>
              </div>
      </td>
      `;
      row.innerHTML = html
  },
};

window.datatable_order = {
  "reviews-for-product":[[0, 'desc']],
  "reviews-for-seller":[[0, 'desc']],
  "seller-table":[[1, 'asc']],
  "recent-purchase":[[2, 'desc']],
  "order-fulfill":[[0, 'desc']],
}