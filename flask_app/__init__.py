from flask import Flask, render_template
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
)
from flask_bcrypt import Bcrypt
from flask_talisman import Talisman

from datetime import datetime
import os

db = MongoEngine()
bcrypt = Bcrypt()
login_manager = LoginManager()


def page_not_found(e):
    return render_template("404.html"), 404


def create_app(test_config=None):

    app = Flask(__name__)

    # load config
    app.config.from_pyfile("config.py", silent=False)
    if test_config is not None:
        app.config.update(test_config)

    # load Flask Mongo, Flask LoginManager, and BCrypt
    from . import db
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    csp = {
        'image-src': 'data:*',
        'style-src': ['\'self\'', 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css', ],
        'script-src': ['\'self\'', 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js', 'https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js', 'https://code.jquery.com/jquery-3.4.1.slim.min.js'],
    }

    Talisman(app,
             content_security_policy=csp,
             content_security_policy_report_uri='/csp_reports'
             )

    from flask_app.users.routes import users
    from flask_app.siteview.routes import site

    # Register blueprints
    app.register_blueprint(users, url_prefix="/users")
    app.register_blueprint(site)

    app.register_error_handler(404, page_not_found)

    login_manager.login_view = "users.login"

    return app
