from models.base_model import BaseModel
import peewee as pw
from models.user import User
from playhouse.hybrid import hybrid_property
from config import S3_LOCATION


class Image(BaseModel):
    image_name = pw.CharField()
    user = pw.ForeignKeyField(User, backref="images")

    @hybrid_property
    def images_url(self):
        return S3_LOCATION + self.image_name
