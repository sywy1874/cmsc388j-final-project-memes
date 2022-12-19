from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

# local imports
from ..forms import NewPost, CommentForm, SearchForm
from ..models import User, Meme, Comment

from ..utils import *

site = Blueprint("site", __name__)


@site.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for('site.search_results', query=form.query.data, query_type=request.form.get("usr_or_post")))

    return render_template('index.html', form=form)


@site.route("/search-results/<query_type>/<query>", methods=["GET"])
def search_results(query, query_type):
    
    try:
        if query_type == "memes":
            results = Meme.objects(title=query)
            meme_pics = []
            for meme in results:
                bytes_im = io.BytesIO(meme.meme_upload.read())
                meme_pic = base64.b64encode(bytes_im.getvalue()).decode()
                meme_pics.append(meme_pic)
            return render_template('query.html', results=results, meme_pics=meme_pics)
        else: # query_type == users
            results = User.objects(username=query)
            propics = []
            for result in results:
                propics.append(get_b64_img(result.username))
            return render_template('user_query.html', results=results, propics=propics)
    except ValueError as error:
        if query_type == "memes":
            return render_template('query.html', error_msg=error)
        else:
            return render_template('user_query.html', error_msg=error)
    



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


@site.route("/meme/<meme_id>", methods=["GET", "POST"])
def meme_detail(meme_id):
    
    meme = Meme.objects(meme_id=meme_id).first()
    error_msg = None
    meme_pic = None
    
    if not meme:
        error_msg="There is no meme to be found here :("
    else:
        bytes_im = io.BytesIO(meme.meme_upload.read())
        meme_pic = base64.b64encode(bytes_im.getvalue()).decode()

    form = CommentForm()
    if form.validate_on_submit() and current_user.is_authenticated:
       comm = Comment(
           for_post=meme,
           commenter=current_user._get_current_object(),
           content=form.text.data,
           date=current_time(),
       )
       comm.save()
       
       return redirect(request.path)

    comments = Comment.objects(for_post=meme)
    commenter_propics = []
    for comment in comments:
        commenter_propics.append(get_b64_img(comment.commenter.username))

    return render_template("meme_detail.html", meme=meme, meme_pic=meme_pic, form=form, comments=comments, commenter_propics=commenter_propics, error_msg=error_msg)


@site.route("/post_meme", methods=["GET", "POST"])
@login_required
def post_meme():
    form = NewPost()

    if form.validate_on_submit():
        print("Categories:", form.categories.data)
        new_memeid = len(Meme.objects) + 1
        meme = Meme(
            poster=current_user._get_current_object(),
            title=form.title.data,
            categories=[form.categories.data],
            meme_id=new_memeid,
            date=current_time(),
        )

        img = form.meme.data
        filename = secure_filename(img.filename)
        content_type = f'images/{filename[-3:]}'

        meme.meme_upload.put(img.stream, content_type=content_type)
        meme.save()

        return redirect(url_for("site.meme_detail", meme_id=new_memeid))

    return render_template("post_meme.html", form=form)


@site.route("/about")
def about():
    return render_template("about.html")
