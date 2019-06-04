from app import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request
from app.forms import RegistrationForm, LoginForm, PostForm, CommentForm
from app.models import User, Post, Comments
from flask_login import current_user, login_user, login_required, logout_user
import os
import secrets
from PIL import Image
from datetime import datetime


@app.route('/')
@app.route('/home')
def home():
    post = Post.query.all()
    form = CommentForm()
    return render_template('home.html', title='Ryan > Brennan', post=post, form=form)

@app.route('/home/<int:post_id>', methods=['POST', 'GET'])
def comment(post_id):
    form = CommentForm()
    post = Post.query.filter_by(id=post_id).first()
    comments = Comments.query.filter_by(post_id=post_id)
    if form.validate_on_submit():
      comment = Comments(body=form.body.data, post_id=post_id)
      db.session.add(comment)
      db.session.commit()
      flash("Comment Posted")
      return redirect(url_for('comment', post_id=post_id))
    return render_template("comments.html", form=form, post=post,comments=comments, title="Comments")
  

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
        return redirect(url_for('login'))
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


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/post_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn


@app.route('/create_post', methods=['POST', 'GET'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.image.data:
            post = Post(body=form.body.data, image=save_picture(form.image.data), date_posted=datetime.now(), author=current_user)
            db.session.add(post)
            db.session.commit()
        else:
            post = Post(body=form.body.data, date_posted=datetime.now(), author=current_user)
            db.session.add(post)
            db.session.commit()
        flash('Post created')
        return redirect(url_for('home'))
    return render_template('post.html', title='Post', form=form)
