from app import app, db, bcrypt
from flask import render_template, url_for, flash, redirect
from app.forms import RegistrationForm
from app.models import User


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Ryan > Brennan')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf_8')
        user = User(username=form.username.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created", "success")
        return redirect(url_for('home'))
    return render_template('registration.html', title='Register', form=form)
