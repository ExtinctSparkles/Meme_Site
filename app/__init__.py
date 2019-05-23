from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dbe48260e4dbcc824ffc7dfabb813ccf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

from app import routes