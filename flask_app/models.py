from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()


class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    profile_pic = db.ImageField()

    # Returns unique string identifying our object
    def get_id(self):
        return self.username


class Meme(db.Document):
    poster = db.ReferenceField(User, required=True)
    title = db.StringField(required=True)
    meme_upload = db.ImageField(size=(1280, 720, True), required=True)
    meme_id = db.IntField(required=True)
    categories = db.ListField(db.StringField())


class Comment(db.Document):
    for_post = db.ReferenceField(Meme, required=True)
    commenter = db.ReferenceField(User, required=True)
    text = db.StringField(required=True)
