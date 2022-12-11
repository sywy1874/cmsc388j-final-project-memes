from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    pass


@users.route("/login", methods=["GET", "POST"])
def login():
    return '<h1>LOGIN PAGE</h1>'


@users.route("/logout")
@login_required
def logout():
    pass


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    pass