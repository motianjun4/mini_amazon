from flask import flash, render_template, request, redirect, url_for
from flask_login import current_user
from app.utils.json_response import ResponseType, json_response
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField, FileField
from wtforms.validators import DataRequired

from .models.cart import Cart
from .models.inventory import Inventory
from .models.purchase import Purchase
from app.models.order import Order
from app.models.user import User
from flask_login import current_user, login_required


from flask import Blueprint
bp = Blueprint('cart', __name__)

class CreateCartForm(FlaskForm):
    address = StringField('Shipping Address', validators=[DataRequired()])
    tel = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Place Order')


@bp.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    cart_list = Cart.get_cart_by_uid_ORM(current_user.id)
    saved_list = Cart.get_saved_by_uid_ORM(current_user.id)
    
    cart_obj_list = [{
        "product":{"pid":cart.inventory.pid, "name":cart.inventory.product.name},
        "seller": {"id":cart.inventory.uid, "name":f"{cart.inventory.seller.firstname} {cart.inventory.seller.lastname}"},
        "cid": cart.id,
        "iid" : cart.iid,
        "price" : f"${cart.inventory.price}",
        "quantity" : cart.quantity,
        "total" : f"${cart.inventory.price * cart.quantity}",
    } for cart in cart_list]

    saved_obj_list = [{
        "product":{"pid":cart.inventory.pid, "name":cart.inventory.product.name},
        "seller": {"id":cart.inventory.uid, "name":f"{cart.inventory.seller.firstname} {cart.inventory.seller.lastname}"},
        "cid": cart.id,
        "iid" : cart.iid,
        "price" : f"${cart.inventory.price}",
        "quantity" : cart.quantity,
        "total" : f"${cart.inventory.price * cart.quantity}",
    } for cart in saved_list]

    total_price = 0
    for cart in cart_list:
        total_price += cart.inventory.price * cart.quantity

    #add form
    form = CreateCartForm()
    if form.validate_on_submit():
        # check balance enough
        if User.check_balance_enough(current_user.id, total_price) == False:
            flash("Balance not enough to place order!")
            return render_template('cart.html',
                            saved_obj_list=saved_obj_list,
                            cart_obj_list=cart_obj_list,
                            user=current_user,
                            total_price=total_price,
                            form=form)
        # check inventory for all items
        iid_list = []
        iid_dict = {}
        for cart in cart_list:
            iid_list.append(cart.inventory.id)
            iid_dict[cart.inventory.id] = cart.quantity
        stock_list = Inventory.get_stock(iid_list)

        out_of_stock_list =  []
        for stock in stock_list:
            if iid_dict[stock[0]] > stock[1]:
                # iid
                out_of_stock_list.append(stock[0])
        # pass all, reduce inventory for each items
        if len(out_of_stock_list) == 0:
            Inventory.reduce_inventory(iid_dict)
        # out of stock, return to front end
        else:
            err_message =  "Place order failed, out of stock for the following ID:"
            for cart in cart_list:
                if cart.iid in out_of_stock_list:
                    err_message += " "+str(cart.id)+","
            err_message=err_message[:-1]+"."
            flash(err_message)
            return render_template('cart.html',
                            saved_obj_list=saved_obj_list,
                            cart_obj_list=cart_obj_list,
                            user=current_user,
                            total_price=total_price,
                            form=form)
        # place order info
        oid = Order.place_order(current_user.id, form.address.data, form.tel.data)
        # place purchase info
        purchase_list = []
        for cart in cart_list:
            purchase_list.append((cart.iid, cart.inventory.price, cart.quantity))
        Purchase.place_order(oid, purchase_list)
        # empty cart
        Cart.empty_cart(current_user.id)
        # reduce deposit
        User.add_balance(current_user.id, -total_price)
        # redirect order page
        return redirect(url_for('order.order_detail', oid=oid))

    return render_template('cart.html',
                        saved_obj_list=saved_obj_list,
                        cart_obj_list=cart_obj_list,
                        user=current_user,
                        total_price=total_price,
                        form=form)

@bp.route("/cart_cnt")
def cart_cnt():
    if current_user.is_authenticated:
        cnt = Cart.get_count(current_user.id)
    else:
        cnt = 0
    return json_response(ResponseType.SUCCESS, {"count":cnt})

@bp.route("/removeCart", methods=['POST'])
@login_required
def remove_cart():
    cid = request.form['cid']
    Cart.delete(cid)
    return json_response(ResponseType.SUCCESS, {"message": "Successfully removed from cart"})

@bp.route("/save_cart_item", methods=['POST'])
@login_required
def save_cart():
    cid = request.form['cid']
    Cart.save_cart_item(cid)
    return json_response(ResponseType.SUCCESS, {"message": "Item has been saved!"})

@bp.route("/add_to_cart", methods=['POST'])
@login_required
def add_to_cart():
    cid = request.form['cid']
    Cart.add_to_cart(cid)
    return json_response(ResponseType.SUCCESS, {"message": "Item has been added to cart!"})

@bp.route("/update_cart_item_quantity", methods=['POST'])
@login_required
def update_cart_item_quantity():
    try:

        cid = request.form['cid']
        quantity = request.form['quantity']
    except:
        return json_response(ResponseType.ERROR, {"message": "cid and quantity required"})
    Cart.update_quantity(cid, quantity)
    return json_response(ResponseType.SUCCESS, {"message": "Successfully updated"})