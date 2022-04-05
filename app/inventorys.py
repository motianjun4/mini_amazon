from cmath import e
from flask import render_template, redirect, request, url_for, flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, IntegerField, FloatField, SubmitField, FileField
from wtforms.validators import DataRequired

import datetime

from app.utils.json_response import ResponseType, json_response

# from .models.purchase import Purchase
# from .models.account import Account
from .models.user import User
from .models.inventory import Inventory
from .models.product import Product

from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
current_user:User

from flask import Blueprint
bp = Blueprint('inventorys', __name__)

# from flask import Blueprint
# bp = Blueprint('accounts', __name__)

class ModifyInventoryForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    submit = SubmitField('Modify!')
    delete = SubmitField('Delete!')

@bp.route('/inventory/<iid>')
def inventory(iid):
    # find the products current user has bought:
    if not current_user.is_authenticated:
        return redirect(url_for('users.login', next=url_for('.inventory')))
    
    form = ModifyInventoryForm()
    inven_iid = Inventory.get_by_iid(current_user.id, iid)
    if form.validate_on_submit():
        # button="submit" if form.submit.data else "delete"
        if form.submit.data:
            Inventory.modify_quantity(form, iid)
        elif form.delete.data:
            Inventory.remove_product(iid)
    return render_template('inventory.html', title='Inventory', inven_iid=inven_iid, form=form)



# @bp.route('/addProduct', methods=['GET', 'POST'])
# @login_required
# def addProduct():
#     pname = None
#     try:
#         pname = request.form['sid']
#     except Exception as e:
#         return json_response(ResponseType.ERROR, None, str(e))
#     pid = Inventory.get_product_pid(pname)
#     Inventory.add_new_product(current_user.id, pid, price=0)
#     return json_response(ResponseType.SUCCESS, {"pid":str(pid)})