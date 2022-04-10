from cmath import e
from traceback import print_list
from unicodedata import decimal, name
from flask import render_template, redirect, request, url_for, flash
from app.models.order import Order
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, IntegerField, FloatField, SubmitField, FileField, ValidationError
from wtforms.validators import DataRequired, NumberRange

import datetime

from app.utils.json_response import ResponseType, json_response

# from .models.purchase import Purchase
# from .models.account import Account
from .models.user import User
from .models.inventory import Inventory
from .models.product import Product

# from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
current_user:User

from flask import Blueprint
bp = Blueprint('inventorys', __name__)

# from flask import Blueprint
# bp = Blueprint('accounts', __name__)

class ModifyInventoryForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Modify!')
    delete = SubmitField('Delete!')

class AddProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(),NumberRange(min=0)])
    price = FloatField('Price', validators=[DataRequired(),NumberRange(min=0)])
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
    # if form.quantity<0 and (type(form.price)==decimal(14,2) and form.price>0)
    # if form.quantity<0 or form.price<0:
    #     return render_template('inventory_add.html', title='Inventory-Adddd', form=form)
    if pid and not Inventory.pid_in_inven(pid, current_user.id):
        if form.validate_on_submit(): 
            Inventory.add_new_product(form, current_user.id, pid)
            return redirect(url_for('users.my_profile'))
    return render_template('inventory_add.html', title='Inventory-Adddd', form=form)
    
        # session['_flashes'].clear()
        
    


@bp.route('/visual_ana')
@login_required
def visual_ana():
    rdlist = Inventory.products_run_down(current_user.id)
    run_down_list = [{
        "iid": run_down.id,
        "pid": run_down.pid,
        "name": run_down.name,
        "price": str(run_down.price),
        "quantity": run_down.quantity,
    } for run_down in rdlist]
    pt_list = Order.products_trends(current_user.id)
    product_trends = [{
        "name": pt[2],
        "num":pt[1],
    }for pt in pt_list]
    return render_template('rundownlist.html',
                           run_down_list=run_down_list,
                           product_trends = product_trends)

@bp.route('/sell_fulfill')
@login_required
def seller_fulfill_rate():
    fulfill_list = Inventory.inventory_fulfill(current_user.id)
    seller_fulfill_list = [
        {"name": item[1], "count": item[0]}
    for item in fulfill_list]
    return json_response(ResponseType.SUCCESS, seller_fulfill_list)