from app import app
from flask import render_template, url_for
from app.forms import RegistrationForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Ryan > Brennan')

@app.route('/registration')
def registration():
  form = RegistrationForm()
  return render_template('registration.html', form=form)
