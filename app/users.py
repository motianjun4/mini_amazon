import datetime
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models.purchase import Purchase

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
    purchases = Purchase.get_all_by_uid_since(
        current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    # render the page by adding information to the index.html file
    return render_template('my_profile.html',
                           purchase_history=purchases,
                           user=current_user)


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
