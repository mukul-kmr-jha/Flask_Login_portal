import uuid
import os
from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# config for SQLAlchemy
app = Flask(__name__)
basedir = os.path.dirname(os.path.realpath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =  os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
# Required for using session
app.secret_key = "some_secret_key"
db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.String(36), primary_key=True)
    fullname=db.Column(db.String(48),nullable=False)
    username=db.Column(db.String(48),unique=True,nullable=False)
    email=db.Column(db.String(80),unique=True,nullable=False)
    phone=db.Column(db.String(15),unique=True,nullable=False)
    password = db.Column(db.String(128),nullable=False)

    # method to store hashed password
    def set_user_id(self):
        self.user_id = str(uuid.uuid4())
    # method to store hashed password
    def set_password(self, password):
        self.password = generate_password_hash(password)
    # method to verify the given password against hashed password
    def check_password(self, password):
        return check_password_hash(self.password,password)
    def get_user_dict(self):
        return {
            "user_id":self.user_id,
            "fullname" : self.fullname,
            "username" : self.username,
            "email" : self.email,
            "phone" : self.phone
        }

    def __repr__(self):
        return f'PERSON :: {self.username} : {self.email} '

# creates the actual table in DB
db.create_all()
