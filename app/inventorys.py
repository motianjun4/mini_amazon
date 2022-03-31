from cmath import e
from flask import render_template, redirect, request, url_for

import datetime

from app.utils.json_response import ResponseType, json_response

# from .models.purchase import Purchase
# from .models.account import Account
from .models.user import User
from .models.inventory import Inventory

from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
current_user:User

from flask import Blueprint
bp = Blueprint('inventorys', __name__)

# from flask import Blueprint
# bp = Blueprint('accounts', __name__)


@bp.route('/inventory')
def inventory():
    # find the products current user has bought:
    if not current_user.is_authenticated:
        return redirect(url_for('users.login', next=url_for('.inventory')))
    # account = Account.get_by_uid(current_user.id)
    inventory = Inventory.get_all_by_uid(current_user.id)
    # render the page by adding information to the index.html file
    return render_template('inventory.html',
                           inventory_history=inventory)