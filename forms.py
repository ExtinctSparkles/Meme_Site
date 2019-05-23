from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired, Length(min=1, max=20)])
    email = StringField('Email', validators=[DataRequired, Email()])
    password = PasswordField('Password', validators=[DataRequired])
    check_password = PasswordField('Check Password', validators=[DataRequired, EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired])
    password = PasswordField('Password', validators=[DataRequired])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login In')