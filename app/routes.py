from app import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request
from app.forms import RegistrationForm, LoginForm, PostForm, CommentForm, EditProfileForm
from app.models import User, Post, Comments, Followers, Following
from flask_login import current_user, login_user, login_required, logout_user
import os
import secrets
from PIL import Image
from datetime import datetime


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    post = Post.query.all()
    return render_template('home.html', title='Ryan > Brennan', post=post)


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
    return render_template("comments.html", form=form, post=post, comments=comments, title="Comments")
  

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
@login_required
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


@app.route('/view_profile/<string:user>', methods=['POST', 'GET'])
def view_profile(user):
    likes = 0
    user = User.query.filter_by(username=user).first_or_404()
    followers = len(user.followers)
    following = len(user.following)

    if user.username == current_user.username:
        currentUser = True
    else:
        currentUser = False
    if user.post:
        post = Post.query.filter_by(user_id=user.id)
        for like in post:
            likes += like.likes
        return render_template('profile.html', title=user.username, posts=post, user=user, likes=likes,name=user.username, followers=followers, following=following, currentUser=currentUser)
    else:
        return render_template('profile.html', title=user.username, user=user, likes=likes, name=user.username, currentUser=currentUser, followers=followers, following=following)


@app.route('/view_profile/<string:user>/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile(user):
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.image.data:
            picture_file = save_picture(form.image.data)
            current_user.image = picture_file
        db.session.commit()
        flash("Changes saved")
        return redirect(url_for("view_profile", user=current_user.username))
    return render_template('edit_profile.html', title="edit_profile", form=form)




@app.route('/home/<int:post_id>/like')
@login_required
def likes(post_id):
    post = Post.query.filter_by(id=post_id).first()
    likes = post.likes
    likes += 1
    post.likes = likes
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/gotohome')
def gohome():
  return redirect(url_for('home'))

@app.route('/view_profile/<string:user>/follow', methods=['GET', 'POST'])
@login_required
def follow(user):
    followed_user = User.query.filter_by(username=user).first()
    follower = Followers(follower=current_user.username, user_id=followed_user.id)
    following = Following(user=user, user_id=current_user.id)
    db.session.add(following)
    db.session.add(follower)
    db.session.commit()
    return redirect(url_for('view_profile', user=user))

@app.route('/view_profile/<string:user>/following')
def following(user):
    u = User.query.filter_by(username=user).first()
    following = u.following
    return render_template('following.html', following=following)

@app.route('/view_profile/<string:user>/followers')
def followers(user):
    u = User.query.filter_by(username=user).first()
    followers = u.followers
    return render_template('followers.html', followers=followers)