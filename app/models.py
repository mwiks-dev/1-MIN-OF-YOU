from sqlalchemy.orm import backref
from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Pitch(db.Model):

    __tablename__ = 'pitches'

    id = db.Column(db.Integer,primary_key=True)
    category = db.Column(db.String)
    context = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    upvote = db.relationship('Upvote',backref='post',lazy='dynamic')
    downvote = db.relationship('Downvote',backref='post',lazy='dynamic')
    comment = db.relationship('Comment',backref='post',lazy='dynamic')

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    def _repr_(self):
        return f'Pitch{self.category}'

    
class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String)
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    pitch_comment = db.Column(db.String)
    posted = db.Column(db.DateTime,default = datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, pitch_id):
        comments = Comment.query.filter_by(pitch_id=pitch_id).all()
        return comments

    @classmethod
    def get_comment_writer(cls, user_id):
        writer = User.query.filter_by(id=user_id).first()

        return writer

class User(UserMixin,db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),unique = True)
    bio = db.Column(db.String(255))
    avatar = db.Column(db.String())
    email = db.Column(db.String(255),unique= True,index = True)
    password_hash = db.Column(db.String(255))
    password_secure = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('You cannnot read the password attribute')
    
    @password.setter
    def password(self, password):
        self.password_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_secure,password)


    def __repr__(self):
        return f'User {self.username}'

class Upvote(db.Model):
    _tablename_ = 'upvotes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_upvotes(cls, id):
        upvote = Upvote.query.filter_by(pitch_id=id).all()
        return upvote

    def _repr_(self):
        return f'{self.user_id}:{self.pitch_id}'


class Downvote(db.Model):
    _tablename_ = 'downvotes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_downvotes(cls, id):
        downvote = Downvote.query.filter_by(pitch_id=id).all()
        return downvote

    def _repr_(self):
        return f'{self.user_id}:{self.pitch_id}'

