from flask import abort, render_template, redirect, send_file, url_for, flash, request
from flask_wtf import FlaskForm
from app.utils.json_response import ResponseType, json_response
from libs.my_minio import get_file

from .models.product import Product
from .models.cart import Cart
from flask_login import current_user, login_required


from flask import Blueprint
bp = Blueprint('misc', __name__)


@bp.route('/img/<name>', methods=['GET'])
def get_image(name):
    path = get_file("image", name)
    if path:
        return send_file(path, "image/jpeg")
    else:
        return abort(404)

@bp.route('/categories', methods=['GET'])
def get_categories():
    return json_response(ResponseType.SUCCESS, Product.get_categories())
