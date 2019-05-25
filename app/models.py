from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(120), nullable=False, default='test_pic.jpg')

    def __repr__(self):
        return "User({}, {}, {})".format(self.id, self.username, self.image)

