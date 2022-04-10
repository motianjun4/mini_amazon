$(function () {
  $('[data-toggle="tooltip"]').tooltip();
});

window.datatables = {};


function format_time(time) {
  let date = new Date(time);
  return `${date.toLocaleString()}`;
}

// key should be used only once in a single page. example: id
function add_cart_button_onclick(key, iid) {
  let quantity_selector = `#key_${key}_quantity`;
  let quantity = $(quantity_selector).val();
  if (quantity < 1) {
    alert("The quantity should be greater than or equal to 1");
    return;
  }
  console.log(iid, quantity);
  add_item_to_cart(iid, quantity);
}


function add_item_to_cart(iid, quantity) {
  $.post("/addCart", { amount: Number(quantity), iid: iid }, (data) => {
    if (data.status != "success") {
      alert("error: " + data.msg);
      return;
    }
    alert(`${quantity} item added!`);
    window.location.href = window.location.href;
  });
}

function update_cart_item_quantity(selector,cid){
  let quantity = $(selector).val();
  if (quantity < 1) {
    alert("The quantity should be greater than or equal to 1");
    return;
  }
  $.post("/update_cart_item_quantity", { cid: cid, quantity: quantity }, (data) => {
    if (data.status != "success") {
      alert("error: " + data.msg);
      return;
    }
    alert(`Quantity updated!`);
    window.location.href = window.location.href;
  });
}

function remove_cart_item(cid) {
  $.post("/removeCart", { cid: cid }, (data) => {
    if (data.status != "success") {
      alert("error: " + data.msg);
      return;
    }
    alert(`Item removed!`);
    window.location.href = window.location.href;
  });
}

function add_to_cart(cid) {
  $.post("/add_to_cart", { cid: cid }, (data) => {
    if (data.status != "success") {
      alert("error: " + data.msg);
      return;
    }
    alert(`Item has been added to cart!`);
    window.location.href = window.location.href;
  });
}

function save_cart_item(cid) {
  $.post("/save_cart_item", { cid: cid }, (data) => {
    if (data.status != "success") {
      alert("error: " + data.msg);
      return;
    }
    alert(`Item has been saved!`);
    window.location.href = window.location.href;
  });
}

function upvote_review(rid, is_upvoted) {
  console.log("upvote review", rid);
  if (is_upvoted) {
    delete_review_like(rid);
    return;
  }
  $.post("/review_like", { rid: rid, action: "upvote" }, (data) => {
    if (data.status != "success") {
      alert("error: " + data.msg);
      return;
    }
    alert(`Review upvoted!`);
    window.location.href = window.location.href;
  });
}

function downvote_review(rid, is_downvoted) {
  console.log("downvote review", rid);
  if (is_downvoted) {
    delete_review_like(rid);
    return;
  }
  $.post("/review_like", { rid: rid, action: "downvote" }, (data) => {
    if (data.status != "success") {
      alert("error: " + data.msg);
      return;
    }
    alert(`Review downvoted!`);
    window.location.href = window.location.href;
  });
}

function delete_review_like(rid) {
  $.ajax({
    url: "/review_like",
    type: "DELETE",
    data: { rid: rid },
    success: function (data) {
      if (data.status != "success") {
        alert("error: " + data.msg);
        return;
      }
      alert(`Canceled!`);
      window.location.href = window.location.href;
    },
  });
}

function confirm_purchase_fulfillment(pid) {
  $.post("/fulfill_purchase", { pid: pid }, (data) => {
    if (data.status != "success") {
      alert("error: " + data.msg);
      return;
    }
    alert(`Order fulfilled!`);
    window.location.href = window.location.href;
  });
}
