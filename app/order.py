from flask import render_template, request
from flask_login import current_user
from app.utils.json_response import ResponseType, json_response

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
        "count": purchase.count
    } for purchase in order.purchases]

    return render_template('order.html', order=order,
                           purchase_obj_list=purchase_obj_list)
