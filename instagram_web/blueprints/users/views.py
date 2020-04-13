from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages
from werkzeug.security import generate_password_hash
from models.user import *
import re

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route("/create", methods=['POST'])
def create():
    name = request.form.get('name')
    password = request.form.get('pass')
    email = request.form.get('email')
    a = User.create(name=name, email=email, password=password)
    if a.save():
        flash('succesfully signed up')
        return redirect(url_for('users.new'))
    else:
        return render_template('users/create.html', email=email, name=name, errors=a.errors)


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
