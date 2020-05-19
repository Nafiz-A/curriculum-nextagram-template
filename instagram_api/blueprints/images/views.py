from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity)
from flask import Blueprint, jsonify, url_for, render_template, request
from models.user import *
from werkzeug.security import check_password_hash
from flask import Flask, request
from flask_login import current_user, login_user, logout_user, LoginManager, login_manager

images_api_blueprint = Blueprint('images_api',
                                __name__,
                                template_folder='templates')


@images_api_blueprint.route('/', methods=["POST"])
# @jwt_required 
def upload():
    current_user=User['33']
    data = request.get_json(silent=True)
    # if "user_file" not in request.files:
    #     return "No user_file key in request.files"

    # file = request.files["user_file"]
    # if file.filename == "":
    #     return "Please select a file"
    # if file:
    #     file.filename = secure_filename(file.filename)
        # output = upload_file_to_s3(file)
        # current_user.update(
            # profile_img=str(output)).execute() 
    return jsonify({'status':success})
