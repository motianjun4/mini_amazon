from flask import render_template, redirect, url_for, flash, request
from .utils.time import localize
from werkzeug.urls import url_parse
from flask_login import login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models.inventory import Inventory
from app.models.review import Review
from app.models.purchase import Purchase
from app.models.order import Order

from app.utils.json_response import ResponseType, json_response

from .models.user import User


from flask import Blueprint
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))


@bp.route('/user')
def my_profile():
    # find the products current user has bought:
    if not current_user.is_authenticated:
        return redirect(url_for('users.login', next=url_for('.my_profile')))
    
    purchases = Purchase.get_all_by_uid(current_user.id).all()
    purchase_obj_list = [{
        "id": purchase.id,
        "product": {"pid": purchase.inventory.product.id, "name": purchase.inventory.product.name},
        "order": {"oid": purchase.oid, "buydate": str(purchase.order.create_at)},
        "price":str(purchase.price),
        "count":purchase.count

    } for purchase in purchases]

    inventory_list = Inventory.get_by_uid_ORM(current_user.id)
    inventory_obj_list = [{
        "iid": item.id,
        "product": {"id": item.product.id, "name": item.product.name},
        "price": str(item.price),
        "quantity": item.quantity,
    } for item in inventory_list]
    is_seller = inventory_list.count() > 0 

    #seller review and product review
    seller_review = Review.show_review_list_user(current_user.id, 1)
    seller_review_obj_list = []
    if seller_review:
        seller_review_obj_list = [{
            "time": str(localize(item[5]).strftime("%m/%d/%Y %H:%M:%S")),
            "seller": {"id": item[4], "name": item[2]+item[3]},
            "rate": item[0],
            "review": item[1],
        } for item in seller_review]
    product_review = Review.show_review_list_user(current_user.id, 2)
    product_review_obj_list = []
    if product_review:
        product_review_obj_list = [{
            "time": str(localize(item[4]).strftime("%m/%d/%Y %H:%M:%S")),
            "product": {"id": item[3], "name": item[2]},
            "rate": item[0],
            "review": item[1],
        } for item in product_review]

    # render the page by adding information to the index.html file
    return render_template('my_profile.html',
                           purchase_obj_list=purchase_obj_list,
                           inventory_obj_list=inventory_obj_list,
                           seller_review_obj_list=seller_review_obj_list,
                           product_review_obj_list=product_review_obj_list,
                           is_seller=is_seller,
                           user=current_user,)


@bp.route('/balance/deposit', methods=['POST'])
@login_required
def deposit():
    amount = None
    try:
        amount = float(request.form['amount'])
    except Exception as e:
        return json_response(ResponseType.ERROR, None, str(e))
    if amount <= 0:
        return json_response(ResponseType.ERROR, None, f'The amount must larger than 0.')
    current_balance = User.add_balance(current_user.id, amount)
    return json_response(ResponseType.SUCCESS, {"current_balance": int(current_balance)})


@bp.route('/balance/withdrawn', methods=['POST'])
@login_required
def withdrawn():
    try:
        amount = float(request.form['amount'])
    except Exception as e:
        return json_response(ResponseType.ERROR, None, str(e))
    if amount > current_user.balance:
        return json_response(ResponseType.ERROR, None, f'${amount} is more than your current balance ${current_user.balance}')
    if amount <= 0:
        return json_response(ResponseType.ERROR, None, f'The amount must larger than 0.')
    current_balance = User.add_balance(current_user.id, -amount)
    return json_response(ResponseType.SUCCESS, {"current_balance": int(current_balance)})


@bp.route('/user/<int:uid>')
def public_profile(uid):
    # show id, name, summary: total number of item buyed, total money spend, 
    # if the user sell something, show email, address*, inventory they have and reviews to that seller
    user = User.get(uid)
    money_spent = Purchase.get_money_spend_by_uid(uid)
    items_bought = Purchase.get_items_bought_by_uid(uid)
    inventory_list = Inventory.get_by_uid_ORM(uid)
    obj_list = [ {
        "product": {"id":item.product.id, "name":item.product.name},
        "price": str(item.price),
    } for item in inventory_list]
    is_seller = inventory_list.count() > 0

    review_obj_list = []
    if is_seller:
        reviews = Review.get_all_by_tuid(uid)
        review_obj_list = [{
            "id": review.id,
            "uid": review.uid,
            "creator": f"{review.user.firstname} {review.user.lastname}",
            "review": review.review,
            "rate": review.rate,
            "upvote_cnt": len(list(filter(lambda item: item.is_up, review.review_likes))),
            "downvote_cnt": len(list(filter(lambda item: not item.is_up, review.review_likes))),
        } for review in reviews]

    # check wether bought this product
    has_bought = Order.bought_from_seller(current_user.id, uid)  
    has_review = False
    review = Review.show_review(current_user.id, 1, uid, 0)
    if review:
        has_review = True

    return render_template('public_profile.html',
                           user=user, 
                           money_spent=money_spent, 
                           items_bought=items_bought, 
                           inventory_list=inventory_list, 
                           is_seller=is_seller,
                           inventory_obj_list = obj_list,
                           review_obj_list=review_obj_list,
                           has_bought=has_bought,
                           review=review,
                           has_review=has_review,
                           )
