from cmath import e
from flask import render_template, redirect, request, url_for

import datetime

from app.utils.json_response import ResponseType, json_response

from .models.purchase import Purchase
from .models.account import Account
from .models.user import User

from flask_login import current_user, login_required
current_user:User

from flask import Blueprint
bp = Blueprint('accounts', __name__)


@bp.route('/account')
def account():
    # find the products current user has bought:
    if not current_user.is_authenticated:
        return redirect(url_for('users.login', next=url_for('.account')))
    account = Account.get_by_uid(current_user.id)
    purchases = Purchase.get_all_by_uid_since(
        current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    # render the page by adding information to the index.html file
    return render_template('account.html',
                           purchase_history=purchases,
                           account=account)

@bp.route('/account/deposit',methods=['POST'])
@login_required
def deposit():
    amount = None
    try:
        amount = float(request.form['amount'])
    except Exception as e:
        return json_response(ResponseType.ERROR, None, str(e))
    current_balance = Account.deposit_by_uid(current_user.id, amount)
    return json_response(ResponseType.SUCCESS, {"current_balance":int(current_balance)})

@bp.route('/account/withdrawn', methods=['POST'])
@login_required
def withdrawn():
    try:
        amount = float(request.form['amount'])
    except Exception as e:
        return json_response(ResponseType.ERROR, None, str(e))
    account = Account.get_by_uid(current_user.id)
    if amount > account.balance:
        return json_response(ResponseType.ERROR, None, f'${amount} is more than your current balance ${account.balance}')
    current_balance = Account.deposit_by_uid(current_user.id, -amount)
    return json_response(ResponseType.SUCCESS, {"current_balance": int(current_balance)})
