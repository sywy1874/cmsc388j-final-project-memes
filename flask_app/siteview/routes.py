from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

# local imports
from ..forms import NewPost, CommentForm
from ..models import User, Meme, Comment

site = Blueprint("site", __name__)


@site.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# In forms.py SearchForm, there is a radio button for whether you want to search a user or a meme
# Make sure to differentiate between that
@site.route("/search-results/<query>", methods=["GET"])
def search_results(query):
    pass



@site.route("/user/<username>")
def user_detail(username):
    pass


# similar to how movie reviews are posted in the projects
# meme_detail should post a comment if the form is validated
# otherwise just display the meme
@site.route("/meme/<memeid>", methods=["GET", "POST"])
def meme_detail(memeid):
    comm = CommentForm()

    if comm.validate_on_submit() and current_user.is_authenticated:
        pass


# the header will have a button to create new post if user is logged in
@site.route("/newmeme", methods=["POST"])
@login_required
def new_meme():
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

    return "<h4>Error while posting meme</h4>"





@site.route("/about")
def about_page():
    pass


# Might need more view functions?