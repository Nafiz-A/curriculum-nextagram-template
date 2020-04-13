from flask import Blueprint, render_template, request, redirect, url_for, session
from models.user import User
from werkzeug.utils import secure_filename
from models.images import Image
from app import app
from instagram_web.blueprints.sessions.upload import *
from config import S3_LOCATION
from flask_login import current_user
from instagram_web.blueprints.sessions.views import *
from instagram_web.blueprints.sessions.upload import *
app.secret_key = 'nothing'


images_blueprint = Blueprint(
    'images', __name__, template_folder='templates'
)
@images_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('images/new.html')


@images_blueprint.route('/create', methods=['POST'])
def create():
    if "user_file" not in request.files:
        return "No user_file key in request.files"
    file = request.files["user_file"]
    output = upload_file_to_s3(file)
    Image.create(image_name=str(output), user_id=User.get_or_none(
        User.email == session['email']).id)
    user = User.get_or_none(User.email == session['email'])

    return render_template('images/create.html', user=user)
