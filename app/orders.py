from uuid import uuid1
from app.models.inventory import Inventory
from app.models.purchase import Purchase
from app.models.user import User
from app.models.order import Order
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, IntegerField, FloatField, SubmitField, FileField
from wtforms.validators import DataRequired
from app.utils.json_response import ResponseType, json_response
from libs.my_minio import put_file

from .models.product import Product
from .models.cart import Cart
from flask_login import current_user, login_required


from flask import Blueprint
bp = Blueprint('orders', __name__)

@bp.route('/orders')
@login_required
def orderlist():
    # show product detail, list of seller and current stock, reviews
    order_obj_list = []
    orders = Order.get_all_by_uid(current_user.id)
    order_obj_list = [{
        "oid": order.id,
        "iid": order.iid,
        "buid": order.buid,
        "name": f"{order.firstname} {order.lastname}",
        "address": order.address,
        "tel": order.tel,
        "create_at": order.create_at,
        # "categories": order.count,
        # "total_amount": order.total_amount,
        "fulfillment": order.fulfillment
    } for order in orders]

    inventory_list = Inventory.get_by_uid_ORM(current_user.id)
    items_bought = Purchase.get_items_bought_by_uid(current_user.id)
    user = User.get(current_user.id)
    money_spent = Purchase.get_money_spend_by_uid(current_user.id)
    is_seller = inventory_list.count() > 0 

    return render_template('order_fulfill.html',
                           order_obj_list=order_obj_list,
                           items_bought = items_bought,
                           user = user,
                           money_spent = money_spent,
                           is_seller = is_seller
                           )