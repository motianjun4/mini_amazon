from wsgiref.validate import validator
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField, FileField
from wtforms.validators import DataRequired
from app.utils.json_response import ResponseType, json_response
from flask_wtf.file import FileAllowed
from uuid import uuid1
from libs.my_minio import put_file

from .models.review import Review, ReviewLike
from flask_login import current_user, login_required


from flask import Blueprint
bp = Blueprint('review', __name__)


class CreateReviewForm(FlaskForm):
    rate = StringField('Rate(Integer Min:0 Max:5)', validators=[DataRequired()])
    review = StringField('Review', validators=[DataRequired()])
    image0 = FileField(u'Image Files: (Optional)', validators=[FileAllowed(['jpg'])])
    image1 = FileField(u'', validators=[FileAllowed(['jpg'])])
    image2 = FileField(u'', validators=[FileAllowed(['jpg'])])
    submit = SubmitField('Submit')

@bp.route('/review/product/submit', methods=['GET', 'POST'])
@login_required
def submitProductReview():
    form = CreateReviewForm()
    if form.validate_on_submit():
        args = request.args        
        rid = Review.submit(current_user.id, 2, 0, args['pid'], form.rate.data, form.review.data)
        for i in range(3):
            key = 'image'+str(i)
            file = request.files[key]
            if file is not None:
                tmp_filepath = f"/tmp/{uuid1()}.jpg"
                file.save(tmp_filepath)
                put_file('image', f'review_{rid}_{i}.jpg', tmp_filepath)
        return redirect(url_for('products.product_detail', pid=args['pid']))
    return render_template('review.html', form=form)

@bp.route('/review/product/edit', methods=['GET', 'POST'])
@login_required
def editProductReview():
    form = CreateReviewForm()
    if form.validate_on_submit():
        args = request.args
        rid = Review.edit(current_user.id, 2, 0, args['pid'], form.rate.data, form.review.data)
        for i in range(3):
            file = request.files['image'+str(i)]
            if file is not None:
                tmp_filepath = f"/tmp/{uuid1()}.jpg"
                file.save(tmp_filepath)
                put_file('image', f'review_{rid}_{i}.jpg', tmp_filepath)
        if args['redirect'] == 'product':
            return redirect(url_for('products.product_detail', pid=args['pid']))
        elif args['redirect'] == 'user':
            return redirect(url_for('users.my_profile'))
    return render_template('review.html', form=form)

@bp.route('/review/product/remove', methods=['GET'])
@login_required
def removeProductReview():
    args = request.args
    Review.delete(current_user.id, 2, 0, args['pid'])
    if args['redirect'] == 'product':
        return redirect(url_for('products.product_detail', pid=args['pid']))
    elif args['redirect'] == 'user':
        return redirect(url_for('users.my_profile'))

@bp.route('/review/seller/submit', methods=['GET', 'POST'])
@login_required
def submitSellerReview():
    form = CreateReviewForm()
    if form.validate_on_submit():
        args = request.args        
        rid = Review.submit(current_user.id, 1, args['sid'], 0, form.rate.data, form.review.data)
        for i in range(3):
            file = request.files['image'+str(i)]
            if file is not None:
                tmp_filepath = f"/tmp/{uuid1()}.jpg"
                file.save(tmp_filepath)
                put_file('image', f'review_{rid}_{i}.jpg', tmp_filepath)
        return redirect(url_for('users.public_profile', uid=args['sid']))
    return render_template('review.html', form=form)

@bp.route('/review/seller/edit', methods=['GET', 'POST'])
@login_required
def editSellerReview():
    form = CreateReviewForm()
    if form.validate_on_submit():
        args = request.args
        rid = Review.edit(current_user.id, 1, args['sid'], 0, form.rate.data, form.review.data)
        for i in range(3):
            file = request.files['image'+str(i)]
            if file is not None:
                tmp_filepath = f"/tmp/{uuid1()}.jpg"
                file.save(tmp_filepath)
                put_file('image', f'review_{rid}_{i}.jpg', tmp_filepath)
        if args['redirect'] == 'seller':
            return redirect(url_for('users.public_profile', uid=args['sid']))
        elif args['redirect'] == 'user':
            return redirect(url_for('users.my_profile'))
    return render_template('review.html', form=form)

@bp.route('/review/seller/remove', methods=['GET'])
@login_required
def removeSellerReview():
    args = request.args
    Review.delete(current_user.id, 1, args['sid'], 0)
    if args['redirect'] == 'seller':
        return redirect(url_for('users.public_profile', uid=args['sid']))
    elif args['redirect'] == 'user':
        return redirect(url_for('users.my_profile'))

@bp.route('/review_like', methods=['POST'])
@login_required
def post_review_like():
    try:
        rid = request.form['rid']
        action = request.form['action']
    except:
        return json_response(ResponseType.ERROR, 'rid and action required')
    if ReviewLike.is_voted(rid, current_user.id):
        ReviewLike.delete(rid, current_user.id)
    if action == 'upvote':
        ReviewLike.insert(rid, current_user.id, 1)
    elif action == 'downvote':
        ReviewLike.insert(rid, current_user.id, 0)
    return json_response(ResponseType.SUCCESS, 'success')

@bp.route('/review_like', methods=['DELETE'])
@login_required
def delete_review_like():
    try:
        rid = request.form['rid']
    except:
        return json_response(ResponseType.ERROR, 'rid and action required')
    ReviewLike.delete(rid, current_user.id)
    return json_response(ResponseType.SUCCESS, 'success')