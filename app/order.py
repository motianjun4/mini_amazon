from flask import render_template, request
from flask_login import current_user
from app.utils.json_response import ResponseType, json_response
from .utils.time import localize, iso, strtime

from .models.order import Order
from flask_login import current_user, login_required


from flask import Blueprint
bp = Blueprint('order', __name__)


@bp.route("/order/<int:oid>")
@login_required
def order_detail(oid):
    order = Order.get(oid)
    order_obj = {
        "id": order.id,
        "user_id": order.user.id,
        "username": f"{order.user.firstname} {order.user.lastname}",
        "create_at": strtime(localize(order.create_at)),
        "address": order.address,
        "tel": order.tel,
    }
    purchase_obj_list = [{
        "id": purchase.id,
        "product": {"pid": purchase.inventory.product.id, "name": purchase.inventory.product.name},
        "order": {"oid": purchase.oid, "buydate": str(purchase.order.create_at)},
        "price": "$"+str(purchase.price),
        "count": purchase.count,
        "sid": purchase.inventory.uid,
        "seller": {"uid": purchase.inventory.uid, "name": purchase.inventory.seller.firstname+" "+purchase.inventory.seller.lastname},
        "fulfillment": "Not Fulfilled" if purchase.fulfillment == False else "Fulfilled at " + strtime(localize(purchase.fulfill_at)),
    } for purchase in order.purchases]

    total_price = 0
    total_fulfill = "Fullfilled"
    for purchase in order.purchases:
        total_price += purchase.count*purchase.price
    for purchase in order.purchases:
        if purchase.fulfillment == False:
            total_fulfill = "Not Fullfilled"
            break

    return render_template('order.html', order_obj=order_obj,
                           purchase_obj_list=purchase_obj_list,
                           total_price=total_price,
                           total_fulfill=total_fulfill)
