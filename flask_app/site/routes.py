from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user

site = Blueprint("site", __name__)


@site.route("/", methods=["GET", "POST"])
def index():
    return '<h1>ITS TIME TO MAKE SOME MEMES</h1>'


@site.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    pass


@site.route("/user/<username>")
def user_detail(username):
    pass


@site.route("/about")
def about_page():
    pass


# Might need more view functions?
