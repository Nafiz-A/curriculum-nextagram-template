from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.payment.views import payment_blueprint
from instagram_web.blueprints.following.views import following_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from google_oauth import oauth

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(payment_blueprint, url_prefix="/payment")
app.register_blueprint(following_blueprint, url_prefix="/following")

oauth.init_app(app)
assets = Environment(app)
assets.register(bundles)
app.config.from_object("config")


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.errorhandler(405)
def internal_server_error(e):
    return render_template('405.html'), 405


@app.errorhandler(404)
def internal_server_error(e):
    return render_template('404.html'), 404


@app.route("/")
def home():
    return render_template('home.html')
