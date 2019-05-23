from app import app
from flask import render_template, url_for
from app.forms import RegistrationForm

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Hello')

@app.route('/registration')
def registration():
  form = RegistrationForm()
  return render_template('registration.html', form=form)
