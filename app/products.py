from uuid import uuid1

from sqlalchemy import false
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
            return redirect(url_for('products.product_manage'))
    return render_template('product_create.html', title='Create Product', form=form)


@bp.route('/searchCart', methods=['GET', 'POST'])
@login_required
def searchCart():
    cart_items = Cart.get_all_by_uid(current_user.id)
    return render_template('main_page.html',
                           cart_items=cart_items)


@bp.route('/product_edit/<pid>', methods=['GET', 'POST'])
@login_required
def product_edit(pid):
    # find the products current user has created:
    form = ProductForm()
    product = Product.get(pid)
    if form.validate_on_submit():
        # button="submit" if form.submit.data else "delete"
        if form.submit.data:
            if not Product.get_all_by_name_ORM(form.product_name.data, pid):
                Product.product_edit(form, pid)
                return redirect(url_for('products.product_manage'))
            flash('Product name existed!')
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


@bp.route('/product/<int:pid>')
@login_required
def product_detail(pid):
    # show product detail, list of seller and current stock, reviews
    product = Product.get(pid)
    seller_list = Inventory.get_seller_list(pid)
    seller_obj_list = [{
        "iid": item[5],
        "seller": {"id": item[4], "name": f"{item[2]} {item[3]}"},
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
        "is_upvote": len(list(filter(lambda item: item.is_up and item.uid == current_user.id, review.review_likes))) > 0,
        "downvote_cnt": len(list(filter(lambda item: not item.is_up, review.review_likes))),
        "is_downvote": len(list(filter(lambda item: not item.is_up and item.uid == current_user.id, review.review_likes))) > 0,
        "create_at": iso(localize(review.create_at)),
    } for review in reviews]

# show summary review
    summary_review = list(Review.show_summary_review(2,0,pid))
    has_summary=False
    has_half=False
    if summary_review[0] is not None:
        has_summary=True
        summary_review.append(int(summary_review[0]))
        if int(summary_review[0]) < summary_review[0]:
            has_half=True
    return render_template('product_detail.html',
                           product=product, 
                           has_bought=has_bought,
                           has_review=has_review,
                           review=review,
                           seller_obj_list=seller_obj_list,
                           review_obj_list=review_obj_list,
                           has_half=has_half,
                           has_summary=has_summary,
                           summary_review = summary_review,
                           )

@bp.route('/addCart', methods=['POST'])
@login_required
def addCart():
    iid_list = []
    iid_list.append(request.form['iid'])
    if iid_list[0] == '':
        return json_response(ResponseType.ERROR, None, "Out of inventory!")
    amount = int(request.form['amount'])
    repo_inventory = Inventory.get_stock(iid_list)[0][1]
    if amount > repo_inventory:
        return json_response(ResponseType.ERROR, None, "Insufficient inventory at this price, click the item to see more details!")
    cart_items = Cart.addCart(iid_list[0], amount)
    return json_response(ResponseType.SUCCESS, {"cart_items":str(cart_items)})
