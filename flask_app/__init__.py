from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
)
from flask_bcrypt import Bcrypt

from datetime import datetime
import os

app = Flask(__name__)

# load config
app.config.from_pyfile("config.py", silent=False)

# load Flask Mongo, Flask LoginManager, and BCrypt
db = MongoEngine(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

from flask_app.users.routes import users
from flask_app.siteview.routes import site

# Register blueprints
app.register_blueprint(users)
app.register_blueprint(site)

login_manager.login_view = "users.login"



    # Test commit vs code to github
