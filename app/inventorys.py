# from cmath import e
# from flask import render_template, redirect, request, url_for

# import datetime

# from numpy import product
# from app.models.inventory import Inventory

# from app.utils.json_response import ResponseType, json_response

# from .models.purchase import Purchase
# from .models.account import Account
# from .models.user import User

# from flask import render_template, redirect, url_for, flash, request
# from werkzeug.urls import url_parse
# from flask_login import login_user, logout_user, current_user, login_required
# from flask_wtf import FlaskForm
# from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField
# from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

# current_user:User

# from flask import Blueprint
# bp = Blueprint('inventorys', __name__)


# class inventoryForm(FlaskForm):
#     product_name = StringField('Product Name', validators=[DataRequired()])
#     product_number = IntegerField('Product Number', validators=[DataRequired()])
#     submit = SubmitField('Add')

# @bp.route('/inventory', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('index.index'))
#     form = inventoryForm()
#     if form.validate_on_submit():
#         if Inventory(form.email.data,
#                          form.password.data,
#                          form.firstname.data,
#                          form.lastname.data):
#             flash('Congratulations, you are now a registered user!')
#             return redirect(url_for('users.login'))
#     return render_template('inventory.html', form=form)

# @bp.route('/inventory')
# def inventory():
#     if not current_user.is_authenticated:
#         return redirect(url_for('users.login', next=url_for('.inventory')))
#     products = Inventory.get(current_user.id)
#     return render_template('inventory.html', avail_products=products)

# @bp.route('/account/deposit',methods=['POST'])
# @login_required
# def deposit():
#     amount = None
#     try:
#         amount = float(request.form['amount'])
#     except Exception as e:
#         return json_response(ResponseType.ERROR, None, str(e))
#     current_balance = Account.deposit_by_uid(current_user.id, amount)
#     return json_response(ResponseType.SUCCESS, {"current_balance":int(current_balance)})