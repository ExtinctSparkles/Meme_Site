from app import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post
from flask_login import current_user, login_user, login_required, logout_user


@app.route('/')
@app.route('/home')
def home():
    post = Post.query.all()
    return render_template('home.html', title='Ryan > Brennan', post=post)


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf_8')
        user = User(username=form.username.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created", "success")
        return redirect(url_for('home'))
    return render_template('registration.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))