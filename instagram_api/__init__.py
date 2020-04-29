from instagram_api.blueprints.users.views import users_api_blueprint
from app import app
from flask_cors import CORS
from flask_wtf import csrf
from flask_wtf.csrf import CSRFError

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##

app.config['JWT_SECRET_KEY'] = 'something_else'

app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')
