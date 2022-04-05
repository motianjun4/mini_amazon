from flask import render_template, request
from flask_login import current_user
from app.utils.json_response import ResponseType, json_response

from .models.cart import Cart
from flask_login import current_user, login_required


from flask import Blueprint
bp = Blueprint('cart', __name__)


@bp.route('/cart')
@login_required
def cart():
    cart_list = Cart.get_all_by_uid_ORM(current_user.id)
    
    cart_obj_list = [{
        "product":{"pid":cart.inventory.pid, "name":cart.inventory.product.name},
        "seller": {"id":cart.inventory.uid, "name":f"{cart.inventory.seller.firstname} {cart.inventory.seller.lastname}"},
        "cid": cart.id,
        "iid" : cart.iid,
        "price" : f"${cart.inventory.price}",
        "quantity" : cart.quantity,
        "total" : f"${cart.inventory.price * cart.quantity}",
    } for cart in cart_list]

    return render_template('cart.html',
                           cart_obj_list=cart_obj_list,
                           user=current_user,)

@bp.route("/cart_cnt")
def cart_cnt():
    if current_user.is_authenticated:
        cnt = Cart.get_count(current_user.id)
    else:
        cnt = 0
    return json_response(ResponseType.SUCCESS, {"count":cnt})

@bp.route("/removeCart", methods=['POST'])
def remove_cart():
    cid = request.form['cid']
    Cart.delete(cid)
    return json_response(ResponseType.SUCCESS, {"message": "Successfully removed from cart"})