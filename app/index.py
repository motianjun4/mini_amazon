from flask import render_template
from flask_login import current_user
import datetime
from .models.product import Product
from .models.cart import Cart
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # get all available products for sale:
    products = Product.get_all(True)
    # find the products current user has bought:
    if current_user.is_authenticated:
        cart_items = Cart.get_all_by_uid(current_user.id)
        cart_cnt = Cart.get_count(current_user.id)
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        cart_items = None
        cart_cnt = None
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases,
                           cart_items=cart_items,
                           cart_cnt=cart_cnt)

