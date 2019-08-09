from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(120), default='default_profile_pic.png')
    bio = db.Column(db.String(120))
    post = db.relationship('Post', backref='author', lazy=True)
    followers = db.relationship('Followers', lazy=True)
    following = db.relationship('Following', lazy=True)

    def __repr__(self):
        return "User({}, {}, {})".format(self.id, self.username, self.image, self.followers, self.following)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(120))
    body = db.Column(db.String(120))
    likes = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comments', lazy=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "Post({}, {}, {})".format(self.image, self.body, self.likes)


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(120), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return "Post({}, {})".format(self.body, self.post_id)


class Followers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "User({}, {})".format(self.follower, self.user_id)

class Following(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "User({}, {})".format(self.body, self.post_id)