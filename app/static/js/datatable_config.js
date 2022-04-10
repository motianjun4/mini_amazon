// Use with datatable.html
// Store configuration separately in this file
window.datatable_config = {
  "my-transactions": [
    {
      title: "ID",
      data: "id",
    },
    {
      title: "Amount",
      data: "amount",
    },
    {
      title: "Type",
      data: "type",
      render: function (data, type, row) {
        return data == 1 ? "Debit" : "Credit";
      },
    },
    {
      title: "Balance",
      data: "balance",
    },
    {
      title: "Create At",
      data: "create_at",
    },
  ],
  "cart-list": [
    {
      title: "ID",
      data: "cid",
    },
    {
      title: "Product",
      data: "product",
      render: (data, type, row) => {
        return `<img style="width:3em; height: 3em; margin-right: 1em" data-src="/img/product_${data.pid}.jpg" /><a href="/product/${data.pid}">${data.name}</a>`;
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
      render: (data, type, row) => {
        if (type != "display") {
          return data;
        }
        return `<input 
                  id="quantity_input_${row.cid}" class="form-control" 
                  type="number" value="${data}" min="1" max="100" onblur="update_cart_item_quantity('#quantity_input_${row.cid}',${row.cid})"
                  data-toggle="tooltip" data-placement="top" title="Click elsewhere to submit"
                  />
                  `;
      },
    },
    {
      title: "Total",
      data: "total",
    },
    {
      title: "Action",
      data: "cid",
      orderable: false,
      width: "17em",

      render: (data, type, row) => {
        return `
        <div class="mb-2"><button class="btn btn-info" onclick="save_cart_item(${data})">Saved for later</button></div>
        <div><button class="btn btn-danger" onclick="remove_cart_item(${data})">Remove</button></div>   
      `;
      },
    },
  ],
  "saved-list": [
    {
      title: "ID",
      data: "cid",
    },
    {
      title: "Product",
      data: "product",
      render: (data, type, row) => {
        return `<img style="width:3em; height: 3em; margin-right: 1em" data-src="/img/product_${data.pid}.jpg" /><a href="/product/${data.pid}">${data.name}</a>`;
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
      render: (data, type, row) => {
        if (type != "display") {
          return data;
        }
        return `<input 
                  id="quantity_input_${row.cid}" class="form-control" 
                  type="number" value="${data}" min="1" max="100" onblur="update_cart_item_quantity('#quantity_input_${row.cid}',${row.cid})"
                  data-toggle="tooltip" data-placement="top" title="Click elsewhere to submit"
                  />
                  `;
      },
    },
    {
      title: "Total",
      data: "total",
    },
    {
      title: "Action",
      data: "cid",
      orderable: false,
      width: "17em",
      render: (data, type, row) => {
        return `  
          <div class="mb-2"><button class="btn btn-info" onclick="add_to_cart(${data})">Add to cart</button></div>
          <div><button class="btn btn-danger" onclick="remove_cart_item(${data})">Remove</button></div>
      `;
      },
    },
  ],
  "product-manage-list": [
    {
      title: "ID",
      data: "product.pid",
    },
    {
      title: "Name",
      data: "product.name",
    },
    {
      title: "Picture",
      data: "product",
      render: (data, type, row) => {
        return `<img style="width:3em; height: 3em; margin-right: 1em" data-src="/img/product_${data.pid}.jpg" /><a href="/product/${data.id}">${data.name}</a>`;
      },
    },
    {
      title: "Category",
      data: "product.category",
    },
    {
      title: "Description",
      data: "product.description",
    },
    {
      title: "Action",
      data: "product",
      orderable: false,
      width: "4em",
      render: (data, type, row) => {
        return `<div><a class="btn btn-sm btn-primary mb-1" style="width:5em" href="/product_edit/${data.pid}">Edit</a></div><div>`;
      },
    },
    // {
    //   title: "Action",
    //   data: "pid",

    //   render: (data, type, row) => {
    //     return `<button class="btn btn-danger" onclick="remove_product_item(${data})">Remove</button>`;
    //   },

    // }
  ],
  "coworker_list": [
    { title: "Name", data: "name" },
    { title: "E-mail", data: "email" },
    {
      title: "Rate",
      data: "rate",
      width: "5em",
      render: (data, type, row) => {
        if (type !== "display") {
          return data;
        }
        return (
          `<i class="bi bi-star-fill"></i>`.repeat(data) +
          `<i class="bi bi-star"></i>`.repeat(5 - data)
        );
      },
    },
  ],
  "coworker_i_list": [
    { title: "Name", data: "name" },
    { title: "E-mail", data: "email" },
    { title: "Total sell number", data: "num" },
  ],
  "product-search-list": [
    {
      title: "Name",
      data: "name",
    },
    {
      title: "Review Rate",
      data: "avgRate",
    },
    {
      title: "Total Sales",
      data: "cnt",
    },
    {
      title: "Lowest Price",
      data: "price",
    }
  ],
  "sell-table": [
    {
      title: "Product",
      data: "product",
      render: (data, type, row) => {
        return `<img style="width:3em; height: 3em; margin-right: 1em" data-src="/img/product_${data.id}.jpg" /><a href="/product/${data.id}">${data.name}</a>`;
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
      title: "Product",
      data: "product",
      render: (data, type, row) => {
        return `<img style="width:3em; height: 3em; margin-right: 1em" data-src="/img/product_${data.pid}.jpg" /><a href="/product/${data.pid}">${data.name}</a>`;
      },
    },
    {
      title: "Seller",
      data: "seller",
      render: (data, type, row) => {
        return `<a href="/user/${data.sid}">${data.name}</a>`;
      },
    },
    {
      title: "Date",
      data: "purchase_time",
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
      title: "Fulfillment",
      data: "fulfillment",
      render: (data, type, row) => {
        if (data === true) {
          return `<span class="badge badge-success">Fulfilled</span>`;
        } else {
          return `<span class="badge badge-warning">Pending</span>`;
        }
      },
    },
    {
      title: "Review",
      data: "review",
      orderable: false,
      render: (data, type, row) => {
        return `<div><a class="btn btn-sm btn-primary mb-1" style="width:5em" href="/user/${data.sid}#my_review">Seller</a></div><div> 
        <a class="btn btn-primary btn-sm" style="width:5em" href="/product/${data.pid}#my_review">Product</a></div>`;
      },
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
        return `<img style="width:3em; height: 3em; margin-right: 1em" data-src="/img/product_${data.pid}.jpg" /><a href="/product_edit/${data.pid}">${data.name}</a>`;
      },
    },
    {
      title: "Seller",
      data: "seller",
      render: (data, type, row) => {
        if (type != "display") {
          return data.name;
        }
        return `<a href="/user/${data.uid}">${data.name}</a>`;
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
    {
      title: "Message",
      data: "seller",
      render: (data, type, row) => {
        return `<a class="btn btn-primary" href="/user/chat/${data.uid}">Send</a>`;
      },
    }
  ],
  "my-inventory": [
    {
      title: "Product",
      data: "product",
      render: (data, type, row) => {
        return `<img style="width:3em; height: 3em; margin-right: 1em" data-src="/img/product_${data.id}.jpg" /><a href="/product/${data.id}">${data.name}</a>`;
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
        return `<a class="btn btn-primary btn-sm mb-1" style="width:5em;" href="/inventory/${data}">Edit</a> <a class="btn btn-danger btn-sm" style="width:5em;" href="/deleteInventory/${data}">Delete</a>`;
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
    { title: "Create At", data: "create_at" },
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
  "run-down-list": [
    {
      title: "Product",
      data: "name",
      render: (data, type, row) => {
        if (type !== "display") {
          return data;
        }
        return `<a href="/product/${row.pid}">${data}</a>`;
      },
    },
    { title: "Price", data: "price" },
    { title: "Quantity", data: "quantity" },
    {
      title: "Action",
      data: "iid",
      orderable: false,
      render: (data, type, row) => {
        return `<a class="btn btn-primary" href="/inventory/${data}">Edit</a>`;
      },
    },
  ],
  product_trend: [
    { title: "Product", data: "name" },
    { title: "Quantity", data: "num" },
  ],
  "reviews-for-product": [
    { title: "Time", data: "time" },
    {
      title: "Product",
      data: "product",
      render: (data, type, row) => {
        return `<img style="width:3em; height: 3em; margin-right: 1em" data-src="/img/product_${data.id}.jpg" /><a href="/product/${data.id}">${data.name}</a>`;
      },
    },
    { title: "Review", data: "review" },
    {
      title: "Images", data: "id",
      render: (data, type, row) => {
        return `
    <img data-src="/img/review_${data}_0.jpg" style="height: 2em; width:2em;">
    <img data-src="/img/review_${data}_1.jpg" style="height: 2em; width:2em;">
    <img data-src="/img/review_${data}_2.jpg" style="height: 2em; width:2em;">`
      }
    },
    {
      title: "Rate",
      data: "rate",
      width: "5em",
      render: (data, type, row) => {
        if (type !== "display") {
          return data;
        }
        return (
          `<i class="bi bi-star-fill"></i>`.repeat(data) +
          `<i class="bi bi-star"></i>`.repeat(5 - data)
        );
      },
    },
    {
      title: "Action",
      data: "product",
      orderable: false,
      render: (data, type, row) => {
        return `<div><a class="btn btn-sm btn-primary mb-1" style="width:5em" href="/review/product/edit?pid=${data.id}&redirect=user">Edit</a></div><div> 
        <a class="btn btn-danger btn-sm" style="width:5em" href="/review/product/remove?pid=${data.id}&redirect=user">Remove</a></div>`;
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
      title: "Images", data: "id",
      render: (data, type, row) => {
        return `
    <img data-src="/img/review_${data}_0.jpg" style="height: 2em; width:2em;">
    <img data-src="/img/review_${data}_1.jpg" style="height: 2em; width:2em;">
    <img data-src="/img/review_${data}_2.jpg" style="height: 2em; width:2em;">`
      }
    },
    {
      title: "Rate",
      data: "rate",
      width: "5em",
      render: (data, type, row) => {
        if (type !== "display") {
          return data;
        }
        return (
          `<i class="bi bi-star-fill"></i>`.repeat(data) +
          `<i class="bi bi-star"></i>`.repeat(5 - data)
        );
      },
    },
    {
      title: "Action",
      data: "seller",
      orderable: false,
      render: (data, type, row) => {
        return `<div><a class="btn btn-sm btn-primary mb-1" style="width:5em" href="/review/seller/edit?sid=${data.id}&redirect=user">Edit</a></div><div> 
        <a class="btn btn-danger btn-sm" style="width:5em" href="/review/seller/remove?sid=${data.id}&redirect=user">Remove</a></div>`;
      },
    },
  ],
};

window.datatable_created_row = {
  "product-search-list": (row, item, index) => {
    row.innerHTML = ""

    html = `
      <td colspan="4">
      <div class="card">
        <div class="card-body" style="display:flex">
            <div>
                <img data-src="/img/product_${item.id}.jpg" style="height: 5em; width:5em;">
            </div>
            
            <div class="ml-2 mr-2" style="flex-grow:1">

                <h4 class="card-title"><span class="badge badge-secondary mr-2">${item.category}</span><a href="/product/${item.id}">${item.name}</a></h4>
                <div class="card-text text-secondary flex" style="justify-content: space-between">
                  <div>
                  ${item.price !== "None" ? "Starting from: $" + item.price : "No seller yet"}
                  </div>
                  <div>
                      Average Rate: ${item.avgRate}/5.00
                  </div>
                  <div>
                      Total Sales: ${item.cnt}
                  </div>
                </div>

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
    row.innerHTML = ""
    html = `
      <td colspan="5">
      <div class="card text-left">
                <div class="card-body">
                  <div class="row">
                    <div class="col">
                      <h4 class="card-title"><span class="text-secondary" style="font-size:0.7em">#${review.id
      } </span><a href="/user/${review.uid}">${review.creator
      }</a>
                      ${window.current_user_id == review.uid
        ? `<span class="text-secondary" style="font-size: 0.7em;">(You)</span>`
        : ""
      }
                      </h4>
                    </div>
                    <div class="col" style="text-align: right;">
                    ${`<i class="bi bi-star-fill"></i>`.repeat(review.rate) +
      `<i class="bi bi-star"></i>`.repeat(5 - review.rate)
      }
                      <button type="button" class="btn ${review.is_upvote ? "btn-dark" : "btn-light"
      }" 
                        onclick="upvote_review(${review.id}, ${review.is_upvote
      })">
                        <i class="bi bi-hand-thumbs-up"></i>${review.upvote_cnt
      }</button>
                      <button type="button" class="btn ${review.is_downvote ? "btn-dark" : "btn-light"
      } mr-2"
                        onclick="downvote_review(${review.id}, ${review.is_downvote
      })">
                        <i class="bi bi-hand-thumbs-down"></i>${review.downvote_cnt
      }</button>
                      
                    </div>
                  </div>
                  <p class="card-text">${review.review}</p>
                  <img data-src="/img/review_${review.id}_0.jpg" style="height: 5em; width:5em;">
                  <img data-src="/img/review_${review.id}_1.jpg" style="height: 5em; width:5em;">
                  <img data-src="/img/review_${review.id}_2.jpg" style="height: 5em; width:5em;">
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
    row.innerHTML = ""
    html = `
      <td colspan="5">
      <div class="card text-left">
                <div class="card-body">
                  <div class="row">
                    <div class="col">
                      <h4 class="card-title">
                      <span class="text-secondary" style="font-size:0.7em">#${review.id
      } </span>
                      <a href="/user/${review.uid}">${review.creator}</a>
                      ${window.current_user_id == review.uid
        ? `<span class="text-secondary" style="font-size: 0.7em;">(You)</span>`
        : ""
      }
                      </h4>
                    </div>
                    <div class="col" style="text-align: right;">
                    ${`<i class="bi bi-star-fill"></i>`.repeat(review.rate) +
      `<i class="bi bi-star"></i>`.repeat(5 - review.rate)
      }
                      <button type="button" class="btn ${review.is_upvote ? "btn-dark" : "btn-light"
      }" 
                        onclick="upvote_review(${review.id}, ${review.is_upvote
      })">
                        <i class="bi bi-hand-thumbs-up"></i>${review.upvote_cnt
      }</button>
                      <button type="button" class="btn ${review.is_downvote ? "btn-dark" : "btn-light"} mr-2"
                        onclick="downvote_review(${review.id}, ${review.is_downvote})">
                        <i class="bi bi-hand-thumbs-down"></i>${review.downvote_cnt
      }</button>
                      
                    </div>
                  </div>
                  <p class="card-text">${review.review}</p>
                  <img data-src="/img/review_${review.id}_0.jpg" style="height: 5em; width:5em;">
                  <img data-src="/img/review_${review.id}_1.jpg" style="height: 5em; width:5em;">
                  <img data-src="/img/review_${review.id}_2.jpg" style="height: 5em; width:5em;">
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
  "reviews-for-product": [[0, 'desc']],
  "reviews-for-seller": [[0, 'desc']],
  "seller-table": [[1, 'asc']],
  "recent-purchase": [[0, 'desc']],
  "order-fulfill": [[0, 'desc']],
  "my-transactions": [[4, 'desc']],
}