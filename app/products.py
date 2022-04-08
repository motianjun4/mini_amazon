from uuid import uuid1
from app.models.inventory import Inventory
from app.models.order import Order
from app.models.review import Review
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, IntegerField, FloatField, SubmitField, FileField
from wtforms.validators import DataRequired
from app.utils.json_response import ResponseType, json_response
from app.utils.time import iso, localize
from libs.my_minio import put_file

from .models.product import Product
from .models.cart import Cart
from flask_login import current_user, login_required


from flask import Blueprint
bp = Blueprint('products', __name__)


@bp.route('/search')
def search():
    args = request.args
    query = args.get("q") or ""
    category = args.get("c") or ""

    if (query is None or query == "") and category == "All":
        product_obj_list = []
        has_result=False
        flash("Please specify searching keyword.")
    else:
        has_result=True
        product_list = Product.get_all_by_keyword(query, f"%{query}%", category if category != "All" else None)
        product_obj_list = [{
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "price": str(product.iMinPrice),
            "iid": product.minPriceIid,
        } for product in product_list]

    categories = Product.get_categories()
    
    return render_template('search.html',
                            user=current_user,
                            has_result=has_result,
                            product_obj_list=product_obj_list,
                            query=query,
                            categories=categories,
                            category=category,
                           )

class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    image = FileField(u'Image File', validators=[FileAllowed(['jpg'])])
    submit = SubmitField('Create!')


@bp.route('/product_create', methods=['GET', 'POST'])
@login_required
def product_create():
    form = ProductForm()
    if form.validate_on_submit():
        file = request.files['image']
        tmp_filepath = f"/tmp/{uuid1()}.jpg"
        file.save(tmp_filepath)
        pid, iid = Product.product_create(form, current_user.id)
        if pid and iid:
            put_file('image', f'product_{pid}.jpg', tmp_filepath)
            flash('Congratulations, you create a new product!')
            return redirect(url_for('index.index'))
    return render_template('product_create.html', title='Create Product', form=form)


@bp.route('/searchCart', methods=['GET', 'POST'])
@login_required
def searchCart():
    cart_items = Cart.get_all_by_uid(current_user.id)
    return render_template('main_page.html',
                           cart_items=cart_items)


@bp.route('/product/<pid>', methods=['GET', 'POST'])
@login_required
def product(pid):
    # find the products current user has created:
    form = ProductForm()
    product = Product.get(pid)
    if form.validate_on_submit():
        # button="submit" if form.submit.data else "delete"
        if form.submit.data:
            Product.product_edit(form, pid)
            return redirect(url_for('products.product_manage'))
        # elif form.delete.data:
        #     Inventory.remove_product(iid)
    return render_template('product_edit.html', title='Modify Product', product=product, form=form)


@bp.route('/product_manage', methods=['GET', 'POST'])
@login_required
def product_manage():
    product_list = Product.get_all_by_uid_ORM(current_user.id)
    product_obj_list = [{
        "product":{"pid":product.id, "name":product.name, "category":product.category, "description":product.description},
    } for product in product_list]
    print(product_obj_list)
    return render_template('product_manage.html',
                        product_obj_list=product_obj_list)


@bp.route('/product_edit/<int:pid>', methods=['GET', 'POST'])
@login_required
def product_edit(pid):
    form = ProductForm()
    if form.validate_on_submit():
        file = request.files['image']
        tmp_filepath = f"/tmp/{uuid1()}.jpg"
        file.save(tmp_filepath)
        pid, iid = Product.product_edit(form, current_user.id)
        if pid and iid:
            put_file('image', f'product_{pid}.jpg', tmp_filepath)
            flash('Congratulations, you edit a product!')
            return redirect(url_for('index.index'))
    return render_template('product_create.html', title='Create Product', form=form)
