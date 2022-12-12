from flask_login import UserMixin
from datetime import datetime
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()


class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)


class Meme(db.Document):
    poster = db.ReferenceField(User, required=True)
    title = db.StringField(required=True)
    meme_upload = db.FileField(required=True)
    post_id = db.IntegerField(required=True, unique=True)
    categories = db.ListField(db.StringField())


class CommentFor(db.Document):
    for_post = db.ReferenceField(Meme, required=True)
    commenter = db.ReferenceField(User, required=True)
    text = db.StringField(required=True)
