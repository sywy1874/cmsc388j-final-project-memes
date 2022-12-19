from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField, SelectField, RadioField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
)

import re
from . import bcrypt

# local imports
from .models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=4, max=20)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is already in use!")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is already in use!")

    def validate_password(self, password):
        pw = password.data

        if len(pw) < 10:
            raise ValidationError(
                "Password must be at least 10 characters long!")

        if not re.search('[a-zA-Z]+', pw):
            raise ValidationError(
                'Password must contain at least one alphabetic character!')

        if not re.search('[0-9]+', pw):
            raise ValidationError(
                'Password must contain at least one numeric character!')


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")


class SearchForm(FlaskForm):
    query = StringField(
        "Search for something...", validators=[InputRequired(), Length(min=4, max=100)]
    )

    usr_or_post = RadioField(
        "Categories", choices=[('users', 'Users'), ('memes', 'Memes')], validators=[InputRequired()]
    )

    submit = SubmitField("Search")


class CommentForm(FlaskForm):
    text = TextAreaField(
        "Comment", validators=[InputRequired(), Length(min=5, max=500)]
    )
    submit = SubmitField("Submit Comment")


class NewPost(FlaskForm):
    title = StringField(
        "Title", validators=[InputRequired(), Length(min=5, max=100)]
    )

    meme = FileField(
        "Upload Meme", validators=[FileRequired(), FileAllowed(['png', 'jpg', 'gif'],
                                                               "Only .png, .jpg, and .gif are supported")]
    )

    categories = SelectField(
        "Categories", choices=[('Wholesome', 'Wholesome'), ('Shitpost', 'Shitpost'), ('Surreal', 'Surreal')]
    )

    submit = SubmitField("Submit Meme!")

    def validate_meme(self, meme):
        # max 16 MB
        max_size = 1024 * 1024 * 16
        if len(meme.data.read()) > max_size:
            raise ValidationError(f"Meme must be less than 16 MB.")

        meme.data.seek(0, 0)

### Change Settings Forms ###


class UpdateUsernameForm(FlaskForm):
    username = StringField('Username', validators=[
        InputRequired(), Length(min=4, max=20)])
    confirm_username = StringField(
        "Confirm Username", validators=[InputRequired(), EqualTo("username")]
    )
    submit = SubmitField('Update Username')

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is already taken")


class UpdateEmailForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    confirm_email = StringField(
        "Confirm Email", validators=[InputRequired(), EqualTo("email")]
    )
    submit = SubmitField('Update Email')

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")


class UpdatePasswordForm(FlaskForm):

    new_password = PasswordField("New Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm New Password", validators=[InputRequired(), EqualTo("new_password")]
    )
    submit = SubmitField('Update Password')

    def validate_new_password(self, new_password):
        pw = new_password.data

        if len(pw) < 10:
            raise ValidationError(
                "Password must be at least 10 characters long!")

        if not re.search('[a-zA-Z]+', pw):
            raise ValidationError(
                'Password must contain at least one alphabetic character!')

        if not re.search('[0-9]+', pw):
            raise ValidationError(
                'Password must contain at least one numeric character!')


class UpdateProfilePicForm(FlaskForm):
    image = FileField('Profile Picture', validators=[
                      FileRequired(), FileAllowed(['jpg', 'png'], 'Images Only!')])
    submit = SubmitField('Update Profile Picture')
