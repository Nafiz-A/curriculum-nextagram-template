from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity)
from flask import Blueprint, jsonify, url_for, render_template, request
from models.user import *
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask import Flask, request
from flask_login import current_user, login_user, logout_user, LoginManager, login_manager
from app import app

users_api_blueprint = Blueprint('users_api',
                                __name__,
                                template_folder='templates')

jwt = JWTManager(app)

#all works fine

@users_api_blueprint.route('/', methods=['GET'])
def users():
    current_user = get_jwt_identity()
    users = User.select()
    return jsonify([{"id": user.id, "username": user.name, "profileImage": user.profile_img} for user in users])

@users_api_blueprint.route('/login', methods=['POST'])
def authorize():
    data = request.get_json(silent=True)
    email = data.get('email')
    password = data.get('password')
    user = User.get_or_none(User.email == email)
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=email)
        login_user(user)
        return jsonify(access_token=access_token)
    return jsonify(message="couldn't log in")

@users_api_blueprint.route('/sign_up', methods=['POST'])
def sign_up():
    data = request.get_json(silent=True)
    print(data)
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if email and password:
        hashed_password = generate_password_hash(password)
        User.create(name=username, email=email, password=hashed_password)
        return jsonify('success')
    return jsonify(message="Try again")

@users_api_blueprint.route('/me<email>')
@jwt_required
def me(email):
    current_user=User.get_or_none(User.email==email)
    return jsonify({"id": current_user.id, "username": current_user.name, "profileImage": current_user.profile_img})

@users_api_blueprint.route('/images/me<email>')
@jwt_required
def images(email):
    current_user=User.get_or_none(User.email==email)
    return jsonify([{'img':i.image_name}for i in current_user.images])

@users_api_blueprint.route('/<id>')
def users_id(id):
    u=User.get_by_id(id)
    return jsonify([{"id": u.id, "username": u.name, "profileImage": u.profile_img },[{'img':i.image_name} for i in u.images]])

@users_api_blueprint.route('/images/all/<ids>')
def all(ids):
    user=User[ids]
    return jsonify([{'img':i.image_name}for i in user.images] )
