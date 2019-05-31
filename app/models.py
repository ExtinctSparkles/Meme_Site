from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(120), default='test_pic.jpg')

    def __repr__(self):
        return "User({}, {}, {})".format(self.id, self.username, self.image)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(120))
    body = db.Column(db.String(120))
    likes = db.Column(db.Integer, default=0)

    def __repr__(self):
        return "Post({}, {}, {})".format(self.image, self.body, self.likes)

