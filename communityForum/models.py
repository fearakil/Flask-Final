from communityForum import app, db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), nullable = False, unique=True)
    email = db.Column(db.String(150), nullable = False, unique = True)
    password = db.Column(db.String(256), nullable = False)
    post = db.relationship('Post', backref = 'author', lazy = True)
    comment = db.relationship('Comment', backref = 'author', lazy = True)

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = self.set_password(password)

    def set_password(self,password):
        """
            Grab the password that is passed into the method
            return the hashed verson of the password 
            which will be stored inside the database
        """
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return self.username, self.email

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __init__(self,title,content,user_id):
        self.title = title
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return self.title, self.content

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow, index=True)

    def __init__(self,text,user_id):
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return self.text

