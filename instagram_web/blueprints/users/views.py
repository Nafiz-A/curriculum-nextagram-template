from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages
from werkzeug.security import generate_password_hash
from models.user import *
import re
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length,Regexp

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

# Bootstrap(app)                            

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(),Regexp('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$',message='Invalid email')])
    name = StringField('name', validators=[InputRequired(), Length(min=5)])
    password = PasswordField('password', validators=[InputRequired(), Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,}$",message='at least one Ucase,L case,number and length 6')])


@users_blueprint.route('/new', methods=['GET','POST'])
def new():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        User.create(name=form.name.data, email=form.email.data, password=hashed_password)
        flash('succesfully signed up')
        return redirect(url_for('users.new'))
    return render_template('users/new.html', form=form)


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
