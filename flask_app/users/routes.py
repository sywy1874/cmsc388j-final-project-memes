from flask import Flask

from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user

from .. import bcrypt
from ..forms import (RegistrationForm, LoginForm,
                     UpdateUsernameForm, UpdateEmailForm, UpdatePasswordForm, UpdateProfilePicForm,)
from ..models import User

from werkzeug.utils import secure_filename

from flask_mail import Mail, Message

from ..utils import *

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("site.index"))

    form = RegistrationForm()

    if form.validate_on_submit():
        

        hashed = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed,
        )

        app = Flask(__name__)

        mail= Mail(app)

        app.config['MAIL_SERVER']='smtp.gmail.com'
        app.config['MAIL_PORT'] = 465
        app.config['MAIL_USERNAME'] = 'ramennoodles408@gmail.com'
        app.config['MAIL_PASSWORD'] = 'aubypindfinoyxgd'
        app.config['MAIL_USE_TLS'] = False
        app.config['MAIL_USE_SSL'] = True
        mail = Mail(app)

        msg = Message('YOU ARE ARE AN OFFICIAL MEMER!', sender = 'ramennoodles408@gmail.com', recipients = [user.email])
        msg.body = "Welcome to Memestagram " + user.username + "!"
        mail.send(msg)
        
        user.save()

        return redirect(url_for("users.login"))

    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("site.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()

        if user is not None and bcrypt.check_password_hash(
                user.password, form.password.data
        ):
            login_user(user)
            return redirect(url_for("site.index", current_user = user))
        else:
            flash("Login failed. Check your username and/or password")
            return redirect(url_for("users.login"))

    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("users.login"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    propic = get_b64_img(current_user.username)

    update_username_form = UpdateUsernameForm()
    update_email_form = UpdateEmailForm()
    update_password_form = UpdatePasswordForm()
    update_propic_form = UpdateProfilePicForm()

    if update_username_form.validate_on_submit():
        current_user.modify(username=update_username_form.username.data)
        current_user.save()

        return redirect(url_for('users.login'))

    if update_email_form.validate_on_submit():
        current_user.modify(email=update_email_form.email.data)
        current_user.save()

        return redirect(url_for('users.login'))

    if update_password_form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(
            update_password_form.new_password.data).decode("utf-8")
        current_user.modify(password=hashed)
        current_user.save()

        return redirect(url_for('users.login'))

    if update_propic_form.validate_on_submit():
        img = update_propic_form.image.data

        filename = secure_filename(img.filename)
        content_type = f'images/{filename[-3:]}'

        if current_user.profile_pic.get() is None:
            current_user.profile_pic.put(img.stream, content_type=content_type)
        else:
            current_user.profile_pic.replace(
                img.stream, content_type=content_type)
        current_user.save()

        return redirect(url_for('users.login'))

    return render_template("account.html", update_username_form=update_username_form, update_email_form=update_email_form, update_password_form=update_password_form, update_propic_form=update_propic_form, image=propic)
