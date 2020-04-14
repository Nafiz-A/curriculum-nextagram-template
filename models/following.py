from models.base_model import BaseModel
import peewee as pw
from models.user import User
from playhouse.hybrid import hybrid_property


class Following(BaseModel):
    user = pw.ForeignKeyField(User)
    follower = pw.ForeignKeyField(User)
    approved = pw.BooleanField(default=False)
