from datetime import datetime
from app.models.inventory import Inventory
from app.models.orm.orm_models import Review
from app.models.purchase import Purchase
from app.models.user import User
from app.models.order import Order
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.utils.json_response import ResponseType, json_response
from app.utils.time import get_now, iso, localize, strtime

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
        "purchase_id": order.purchase_id,
        "product": {"pid": order.pid, "name": order.product_name},
        "product_name": order.product_name,
        "buyer": {"uid": order.buid, "name": f"{order.firstname} {order.lastname}"},
        "address": order.address,
        "tel": order.tel,
        "create_at": strtime(localize(order.create_at)),
        # "categories": order.count,
        "total_amount": order.total_amount,
        "fulfillment": order.fulfillment
    } for order in orders]

    # cnt = 0
    # total_amount = 0
    # for order in orders:
    #     if order.uid == current_user.id:
    #         cnt+=1
    #         total_amount += order.count

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


@bp.route('/co_worker')
@login_required
def co_worker():
    cw_list = Order.analy_buyer(current_user.id)
    cws = [{
        "name": cw[0],
        "email": cw[1],
        "rate": cw[2]
    } for cw in cw_list]

    cws_i_list = Order.analy_buyer_i(current_user.id)
    cws_i = [{
        "name": cwi[0],
        "email": cwi[1],
        "num": cwi[2]
    }for cwi in cws_i_list]
    return render_template('coworker.html',
                           cws=cws, 
                           cws_i=cws_i)

# get rating of buyers
@bp.route('/rating_buyer')
@login_required
def buyer_rates_data():
    rate_list = Order.get_score_by_uid(current_user.id)
    buyer_rating_list = [
        {"name": item[0], "count": item[1]}
    for item in rate_list]
    return json_response(ResponseType.SUCCESS, buyer_rating_list)

@bp.route('/sell_history')
@login_required
def balance_history_data():
    sell_history = Order.get_shis_by_uid(current_user.id)
    sell_list = [
        [strtime(item[0]), float(str(item[1]))]
    for item in sell_history]
    return json_response(ResponseType.SUCCESS, sell_list)

@bp.route('/fulfill_purchase', methods=['POST'])
@login_required
def fulfill_purchase():
    pid = request.form.get('pid')
    if pid is None:
        return json_response(ResponseType.ERROR, "pid is required")
    Purchase.fulfill(pid, get_now())
    return json_response(ResponseType.SUCCESS, "purchase fulfilled")

