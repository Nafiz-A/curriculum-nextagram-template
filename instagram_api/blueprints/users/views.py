from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity)
from flask import Blueprint, jsonify, url_for, render_template, request
from models.user import *
from werkzeug.security import check_password_hash
from flask import Flask, request

users_api_blueprint = Blueprint('users_api',
                                __name__,
                                template_folder='templates')

jwt = JWTManager(app)


@users_api_blueprint.route('/', methods=['GET'])
@jwt_required
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
        print('entered')
        return jsonify(access_token=access_token)
    return jsonify(message="couldn't log in")
