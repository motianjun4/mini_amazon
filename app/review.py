from wsgiref.validate import validator
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField, FileField
from wtforms.validators import DataRequired
from app.utils.json_response import ResponseType, json_response
from libs.my_minio import minio_client

from .models.review import Review
from flask_login import current_user, login_required


from flask import Blueprint
bp = Blueprint('review', __name__)


class CreateReviewForm(FlaskForm):
    rate = StringField('Rate', validators=[DataRequired()])
    review = StringField('Review', validators=[DataRequired()])
    submit = SubmitField('Submit')

@bp.route('/review/product/submit', methods=['GET', 'POST'])
@login_required
def submitProductReview():
    form = CreateReviewForm()
    if form.validate_on_submit():
        args = request.args        
        Review.submit(args['uid'], 2, 0, args['pid'], form.rate.data, form.review.date)
        return url_for('index.index')
    return render_template('review.html', form=form)

@bp.route('/review/product/edit', methods=['GET', 'POST'])
@login_required
def editProductReview():
    form = CreateReviewForm()
    if form.validate_on_submit():
        args = request.args
        Review.edit(args['uid'], 2, 0, args['pid'], form.rate.data, form.review.date)
        return url_for('index.index')
    return render_template('review.html', form=form)

@bp.route('/review/product/remove', methods=['POST'])
@login_required
def removeProductReview():
    args = request.args
    Review.delete(args['uid'], 2, 0, args['pid'])
    return json_response(ResponseType.SUCCESS, {})

@bp.route('/review/seller/submit', methods=['GET', 'POST'])
@login_required
def submitSellerReview():
    form = CreateReviewForm()
    if form.validate_on_submit():
        args = request.args        
        Review.submit(args['uid'], 1, args['sid'], 0, form.rate.data, form.review.date)
        return url_for('index.index')
    return render_template('review.html', title='SubmitReview', form=form)

@bp.route('/review/seller/edit', methods=['GET', 'POST'])
@login_required
def editSellerReview():
    form = CreateReviewForm()
    if form.validate_on_submit():
        args = request.args
        Review.edit(args['uid'], 1, args['sid'], 0, form.rate.data, form.review.date)
        return url_for('index.index')
    return render_template('review.html', title='EditReview', form=form)

@bp.route('/review/seller/remove', methods=['POST'])
@login_required
def removeProductReview():
    args = request.args
    Review.delete(args['uid'], 1, args['sid'], 0)
    return json_response(ResponseType.SUCCESS, {})