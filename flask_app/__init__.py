from flask import Flask, render_template
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
)
from flask_bcrypt import Bcrypt

from datetime import datetime
import os

db = MongoEngine()
bcrypt = Bcrypt()
login_manager = LoginManager()


def page_not_found(e):
    return render_template("404.html"), 404

def create_app(test_config="config.py"):

    app = Flask(__name__)

    # load config
    app.config.from_pyfile(test_config, silent=False)

    # load Flask Mongo, Flask LoginManager, and BCrypt
    from . import db
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from flask_app.users.routes import users
    from flask_app.siteview.routes import site

    # Register blueprints
    app.register_blueprint(users, url_prefix="/users")
    app.register_blueprint(site)

    app.register_error_handler(404, page_not_found)

    login_manager.login_view = "users.login"

    return app
