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
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,)

