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

@bp.route('/product/<int:pid>')
@login_required
def product_detail(pid):
    # show product detail, list of seller and current stock, reviews
    product = Product.get(pid)

    seller_list = Inventory.get_seller_list(pid)
    seller_obj_list = [{
        "seller": {"id": item[4], "name": item[2] + item[3]},
        "price": str(item[0]),
        "quantity": str(item[1]),
    } for item in seller_list]

    # check wether bought this product
    has_bought = False
    order_list = Order.order_page(current_user.id)
    for order in order_list:
        if(order[2] == pid):
            has_bought = True

    has_review = False
    review = Review.show_review(current_user.id, 2, 0, pid)
    if review:
        has_review = True

    review_obj_list = []
    reviews = Review.get_all_by_tpid(pid)
    review_obj_list = [{
        "id": review.id,
        "uid": review.uid,
        "creator": f"{review.user.firstname} {review.user.lastname}",
        "review": review.review,
        "rate": review.rate,
        "upvote_cnt": len(list(filter(lambda item: item.is_up, review.review_likes))),
        "downvote_cnt": len(list(filter(lambda item: not item.is_up, review.review_likes))),
    } for review in reviews]

    return render_template('product_detail.html',
                           product=product, 
                           has_bought=has_bought,
                           has_review=has_review,
                           review=review,
                           seller_obj_list=seller_obj_list,
                           review_obj_list=review_obj_list,
                           )