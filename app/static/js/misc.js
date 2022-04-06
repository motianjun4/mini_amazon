
// key should be used only once in a single page. example: id
function add_cart_button_onclick(key, iid){
    let quantity_selector = `#key_${key}_quantity`;
    let quantity = $(quantity_selector).val();
    if (quantity < 1) {
      alert("The quantity should be greater than or equal to 1");
      return;
    }
    console.log(iid, quantity)
    add_item_to_cart(iid, quantity);
}

function add_item_to_cart(iid, quantity) {
  $.post("/addCart", { amount: Number(quantity), iid: iid }, (data) => {
    if (data.status != "success") {
      alert("error: " + data.msg);
      return;
    }
    alert(`${quantity} item added!`);
    location.reload();
  });
}

function remove_cart_item(cid) {
  $.post("/removeCart", { cid: cid }, (data) => {
    if (data.status != "success") {
      alert("error: " + data.msg);
      return;
    }
    alert(`Item removed!`);
    location.reload();
  });
}

function upvote_review(rid, is_upvoted) {
  console.log("upvote review", rid);
  if (is_upvoted) {
    delete_review_like(rid);
    return;
  }
  $.post("/review_like", { rid: rid, action:"upvote" }, (data) => {
    if (data.status != "success") {
      alert("error: " + data.msg);
      return;
    }
    alert(`Review upvoted!`);
    location.reload();
  });
}

function downvote_review(rid, is_downvoted) {
  console.log("downvote review", rid);
  if (is_downvoted){
    delete_review_like(rid);
    return;
  }
  $.post("/review_like", { rid: rid, action: "downvote" }, (data) => {
    if (data.status != "success") {
      alert("error: " + data.msg);
      return;
    }
    alert(`Review downvoted!`);
    location.reload();
  });
}

function delete_review_like(rid) {
  $.ajax({
    url: "/review_like",
    type: "DELETE",
    data: { rid: rid },
    success: function(data) {
      if (data.status != "success") {
        alert("error: " + data.msg);
        return;
      }
      alert(`Canceled!`);
      location.reload();
    }})

}

function confirm_purchase_fulfillment(pid){
  $.post("/fulfill_purchase", { pid: pid }, (data) => {
    if (data.status != "success") {
      alert("error: " + data.msg);
      return;
    }
    alert(`Order fulfilled!`);
    location.reload();
  });
}