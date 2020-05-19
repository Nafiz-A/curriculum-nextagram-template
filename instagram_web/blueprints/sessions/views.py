from google_oauth import oauth
from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages, session
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from models.user import *
from app import app
from .upload import *
from flask_login import current_user, login_user, logout_user, LoginManager, login_manager
from config import S3_LOCATION
from wtforms import form
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length,Regexp

app.secret_key = 'nothing'


sessions_blueprint = Blueprint(
    'sessions', __name__, template_folder='templates'
)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6)])
    remember = BooleanField('remember me')

@sessions_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('sessions.profile'))
    if form.validate_on_submit():
        user = User.get(email=form.email.data)
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('sessions.profile'))
        return render_template('sessions/login.html', form=form)

    return render_template('sessions/login.html', form=form)

       

@sessions_blueprint.route('/profile')
def profile():
    if current_user.is_authenticated:
        return render_template('sessions/profile_page.html', current_user=current_user)
    else:
        return redirect(url_for('sessions.login'))


@sessions_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('sessions.login'))


@sessions_blueprint.route('/upload', methods=["POST"])
def upload_file():
    if "user_file" not in request.files:
        return "No user_file key in request.files"

    file = request.files["user_file"]
    if file.filename == "":
        return "Please select a file"
    if file:
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file)
        User.get_or_none(User.email == current_user.email).update(
            profile_img=str(output)).execute()
        return render_template('images/new.html', output=output)


@sessions_blueprint.route('/main', methods=["POST"])
def main():
    pass


@sessions_blueprint.route("/google_login")
def google_login():
    redirect_uri = url_for('sessions.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@sessions_blueprint.route("/authorize/google")
def authorize():
    oauth.google.authorize_access_token()
    email = oauth.google.get(
        'https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)
    if user:
        login_user(user)
        return redirect(url_for('sessions.profile'))
    else:
        return redirect('sessions/new')
