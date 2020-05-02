from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime
from playhouse.hybrid import hybrid_property
from app import app
from flask_login import UserMixin, LoginManager, login_manager
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


login_manager = LoginManager()

login_manager.init_app(app)


class User(BaseModel, UserMixin):
    name = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.TextField(null=False)
    profile_img = pw.CharField(null=True)

    def save(self, *args, **kwargs):
        self.errors = []
        # self.validate()

        if len(self.errors) == 0:
            self.updated_at = datetime.now()
            return super(BaseModel, self).save(*args, **kwargs)
        else:
            return 0

    def validate(self):
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if(len(self.name) < 5):
            self.errors.append('username length less than 5')
        if(not re.search(regex, self.email)):
            self.errors.append('email invalid')
        if(not re.match(r'[A-Za-z0-9@#$%^*&+!=]{6,}', self.password)):
            self.errors.append(
                'pass must have Ucase,L case,special char,number and length of at least 6')
        else:
            self.password = generate_password_hash(self.password)

    @hybrid_property
    def profile_image_url(self):
        # return app.config.get('S3_LOCATION')+self.profile_image
        return S3_LOCATION + self.profile_image

    @hybrid_property
    def followers(self):
        from models.following import Following
        return User.select().join(Following, on=(User.id == Following.follower_id)).where((Following.user_id == self.id)&(Following.approved!=True))
    
    @hybrid_property
    def is_followers(self):
        from models.following import Following
        return User.select().join(Following, on=(User.id == Following.follower_id)).where((Following.user_id == self.id)&(Following.approved==True))

    @hybrid_property
    def following(self):
        from models.following import Following
        return User.select().join(Following, on=(User.id == Following.user_id)).where((Following.follower_id == self.id)&(Following.approved!=True))

    @hybrid_property
    def is_following(self):
        from models.following import Following
        return User.select().join(Following, on=(User.id == Following.user_id)).where((Following.follower_id == self.id)&(Following.approved==True))

@login_manager.user_loader
def load_user(user_id):
    return  User.get_or_none(id=user_id)
