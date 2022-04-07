from cmath import e
from unicodedata import name
from flask import render_template, redirect, request, url_for, flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, IntegerField, FloatField, SubmitField, FileField, ValidationError
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

class AddProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    add = SubmitField('ADD!')

@bp.route('/inventory/<iid>', methods=['GET', 'POST'])
@login_required
def inventory(iid):
    # find the products current user has bought:
    # if not current_user.is_authenticated:
    #     return redirect(url_for('users.login', next=url_for('.inventory')))
    
    form = ModifyInventoryForm()
    inven_iid = Inventory.get_by_iid(current_user.id, iid)
    if form.validate_on_submit():
        # button="submit" if form.submit.data else "delete"
        if form.submit.data:
            Inventory.modify_quantity(form, iid)
            return redirect(url_for('users.my_profile'))
        # elif form.delete.data:
        #     Inventory.remove_product(iid)
    return render_template('inventory.html', title='Inventory', inven_iid=inven_iid, form=form)

@bp.route('/deleteInventory/<iid>', methods=['GET', 'POST'])
@login_required
def deleteInventory(iid):
    Inventory.remove_product(iid)
    return redirect(url_for('users.my_profile'))

@bp.route('/addInventory', methods=['GET', 'POST'])
@login_required
def addProduct():
    form = AddProductForm()
    pid = Inventory.get_product_pid(form)
    if pid:
        if form.validate_on_submit():
            Inventory.add_new_product(form, current_user.id, pid)
            return redirect(url_for('users.my_profile'))
    return render_template('inventory_add.html', title='Inventory-Adddd', form=form)
#     pname = None
#     try:
#         pname = request.form['sid']
#     except Exception as e:
#         return json_response(ResponseType.ERROR, None, str(e))
#     pid = Inventory.get_product_pid(pname)
#     Inventory.add_new_product(current_user.id, pid, price=0)
#     return json_response(ResponseType.SUCCESS, {"pid":str(pid)})
@bp.route('/runningdown')
@login_required
def runningdown():
    rdlist = Inventory.products_run_down(current_user.id)
    run_down_list = [{
        "iid": run_down.id,
        "pid": run_down.pid,
        "name": run_down.name,
        "price": str(run_down.price),
        "quantity": run_down.quantity,
    } for run_down in rdlist]
    return render_template('rundownlist.html',
                           run_down_list=run_down_list)