from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

# local imports
from ..forms import SearchForm, NewPost, CommentForm
from ..models import User, Meme, Comment

from ..utils import *

site = Blueprint("site", __name__)


## NOTE: UNFINISHED
@site.route("/", methods=["GET"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("query_results", query=form.search_query.data))

    return render_template("index.html", form=form)


# In forms.py SearchForm, there is a radio button for whether you want to search a user or a meme
# Make sure to differentiate between that

## NOTE: UNFINISHED
@site.route("/search-results/<query>", methods=["GET"])
def search_results(query):
    try:
        results = search(query)
    except ValueError as e:
        return render_template("query.html", error_msg=str(e))

    return render_template("query.html", results=results)


## NOTE: UNFINISHED
@site.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    propic = get_b64_img(user.username)
    posts = None
    posts_count = 0
    error_msg = None
    if user is None:
        error_msg = f"User {username} not found"
    else:
        posts = Meme.objects(poster=user)
        posts_count = len(posts)

    return render_template('user_detail.html', user=user, image=propic, posts=posts, posts_count=posts_count, error_msg=error_msg)


# similar to how movie reviews are posted in the projects
# meme_detail should post a comment if the form is validated
# otherwise just display the meme

## NOTE: UNFINISHED
@site.route("/meme/<memeid>", methods=["GET", "POST"])
def meme_detail(memeid):
    comm = CommentForm()

    if comm.validate_on_submit() and current_user.is_authenticated:
        pass


# the header will have a button to create new post if user is logged in
@site.route("/post_meme", methods=["GET", "POST"])
@login_required
def post_meme():
    form = NewPost()

    if form.validate_on_submit():
        new_memeid = len(Meme.objects) + 1
        meme = Meme(
            poster=current_user._get_current_object(),
            title=form.title.data,
            categories=form.categories.data,
            meme_id=new_memeid
        )

        img = form.meme.data
        filename = secure_filename(img.filename)
        content_type = f'images/{filename[-3:]}'

        meme.meme_upload.put(img.stream, content_type=content_type)
        meme.save()

        return redirect(url_for("site.meme_detail", memeid=new_memeid))

    return render_template("post_meme.html", form=form)
    #return "<h4>Error while posting meme</h4>"


@site.route("/about")
def about():
    return render_template("about.html")
