from app import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request
from app.forms import RegistrationForm, LoginForm, PostForm
from app.models import User, Post
from flask_login import current_user, login_user, login_required, logout_user
import os
import secrets
from PIL import Image


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


def save_picture(picture_file):
    rand_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture_file.filename)
    picture_fn = rand_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_images', picture_fn)
    output_size = (125, 125)
    i = Image.open(output_size)
    i.save(picture_path)
    return picture_fn


@app.route('/create_post', methods=['POST', 'GET'])
@login_required
def create_post():
    global post
    form = PostForm()
    if form.validate_on_submit():
        if form.image.data:
            picture = save_picture(form.image.data)
            post = Post(body=form.body.data, image=picture)
        else:
            post = Post(body=form.body.data)
        db.session.add(post)
        db.session.commit()
        flash('Post created')
        return redirect(url_for('home'))
    return render_template('post.html', title='Post', form=form)

