
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