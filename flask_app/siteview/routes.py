from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required

site = Blueprint("site", __name__)


@site.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@site.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    pass


@site.route("/user/<username>")
def user_detail(username):
    pass


@site.route("/newpost")
@login_required
def new_post():
    pass


@site.route("/about")
def about_page():
    pass


# Might need more view functions?