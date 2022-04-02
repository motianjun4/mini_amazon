from uuid import uuid1
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
bp = Blueprint('products', __name__)



class CreateProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    image = FileField(u'Image File', validators=[FileAllowed(['jpg'])])
    submit = SubmitField('Create!')


@bp.route('/sell', methods=['GET', 'POST'])
@login_required
def createProduct():
    form = CreateProductForm()
    if form.validate_on_submit():
        file = request.files['image']
        tmp_filepath = f"/tmp/{uuid1()}.jpg"
        file.save(tmp_filepath)
        pid, iid = Product.createProduct(form, current_user.id)
        if pid and iid:
            put_file('image', f'product_{pid}.jpg', tmp_filepath)
            flash('Congratulations, you create a new product!')
            return redirect(url_for('index.index'))
    return render_template('sell.html', title='Sell', form=form)


@bp.route('/addCart', methods=['GET', 'POST'])
@login_required
def addCart():
    sid = None
    amount = None
    try:
        sid = request.form['sid']
        amount = int(request.form['amount'])
    except Exception as e:
        return json_response(ResponseType.ERROR, None, str(e))
    cart_items = Cart.addCart(sid, amount)
    return json_response(ResponseType.SUCCESS, {"cart_items":str(cart_items)})


@bp.route('/searchCart', methods=['GET', 'POST'])
@login_required
def searchCart():
    cart_items = Cart.get_all_by_uid(current_user.id)
    return render_template('main_page.html',
                           cart_items=cart_items)