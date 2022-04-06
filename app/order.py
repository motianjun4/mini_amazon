from flask import render_template, request
from flask_login import current_user
from app.utils.json_response import ResponseType, json_response
from .utils.time import localize

from .models.order import Order
from flask_login import current_user, login_required


from flask import Blueprint
bp = Blueprint('order', __name__)


@bp.route("/order/<int:oid>")
@login_required
def order_detail(oid):
    order = Order.get(oid)
    purchase_obj_list = [{
        "id": purchase.id,
        "product": {"pid": purchase.inventory.product.id, "name": purchase.inventory.product.name},
        "order": {"oid": purchase.oid, "buydate": str(purchase.order.create_at)},
        "price": "$"+str(purchase.price),
        "count": purchase.count,
        "sid": purchase.inventory.uid,
        "fulfillment": "Not Fulfilled" if purchase.fulfillment == False else "Fulfilled at " + str(localize(purchase.fulfill_at).strftime("%m/%d/%Y %H:%M:%S")),
    } for purchase in order.purchases]

    total_price = 0
    total_fulfill = "Fullfilled"
    for purchase in order.purchases:
        total_price += purchase.count*purchase.price
    for purchase in order.purchases:
        if purchase.fulfillment == False:
            total_fulfill = "Not Fullfilled"
            break

    return render_template('order.html', order=order,
                           purchase_obj_list=purchase_obj_list,
                           total_price=total_price,
                           total_fulfill=total_fulfill)
