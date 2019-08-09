from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    check_password = PasswordField('Check Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken please choose a different one')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is taken please choose a different one')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login In')


class PostForm(FlaskForm):
    body = StringField('Body', validators=[Length(min=5, max=100)])
    image = FileField('Image File', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    submit = SubmitField('Create Post')


class CommentForm(FlaskForm):
    body = StringField('Comment', validators=[Length(min=1, max=120), DataRequired()])
    submit = SubmitField('Post Comment')

class EditProfileForm(FlaskForm):
    username = StringField('Username')
    image = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    bio = StringField('Bio')
    submit = SubmitField('Save Changes')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken please choose a different one')

