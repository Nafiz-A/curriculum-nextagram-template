from flask import Blueprint, render_template, request
from werkzeug.security import generate_password_hash
from flask_wtf.csrf import CSRFProtect
# csrf = CSRFProtect()
users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route("/sign_up", methods=['POST'])
def sign_up():
    username = request.form.get('username')
    password = request.form.get('pass')
    hashed = generate_password_hash(password)
    return render_template('users/sign_up.html', username=request.form.get('username'), hashed=generate_password_hash(password))


@users_blueprint.route('/', methods=['POST'])
def create():
    pass


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
