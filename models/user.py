from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime
from playhouse.hybrid import hybrid_property
from app import app
from flask_login import UserMixin, LoginManager

login_manager = LoginManager()

login_manager.init_app(app)


class User(BaseModel, UserMixin):
    name = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.TextField(null=False)
    profile_img = pw.CharField(null=True)

    def save(self, *args, **kwargs):
        self.errors = []
        self.validate()

        if len(self.errors) == 0:
            self.updated_at = datetime.now()
            return super(BaseModel, self).save(*args, **kwargs)
        else:
            return 0

    def validate(self):
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if(len(self.name) < 8):
            self.errors.append('less than 8')
        if(not re.search(regex, self.email)):
            self.errors.append('email invalid')
        if(not re.match(r'[A-Za-z0-9@#$%^*&+!=]{8,}', self.password)):
            self.errors.append(
                'pass must hv Ucase,lcase,special char,number and length of at least 8')
        else:
            self.password = generate_password_hash(self.password)

    @hybrid_property
    def profile_image_url(self):
        return S3_LOCATION + self.profile_image

    @login_manager.user_loader
    def load_user(email):
        if not User.get_or_none(User.email == email):
            return
        user = User()
        user.id = email
        return user

    @login_manager.request_loader
    def request_loader(request):
        email = request.form.get('email')
        if not User.get_or_none(User.email == email):
            return
        user = User()
        user.id = email
        # user.is_authenticated == False
        return user
