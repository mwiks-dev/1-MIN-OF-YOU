from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

@login_manager.user_loader
def load_user(user):
    return User.get(user)

class Pitch(db.Model):

    __tablename__ = 'pitches'

    id = db.Column(db.Integer,primary_key=True)
    category = db.Column(db.String(25))
    context = db.Column(db.String)
    uploadedBy = db.Column(db.String(10))
    posted = db.Column(db.DateTime,default=datetime.utcnow)

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    
class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key=True)
    pitch_id = db.Column(db.Integer)
    pitch_comment = db.Column(db.String)
    posted = db.Column(db.DateTime,default = datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()


class User(UserMixin,db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20))
    bio = db.Column(db.String(50))
    avatar = db.Column(db.String())
    email = db.Column(db.String(20),unique= True,index = True)
    password_hash = db.Column(db.String(20))
    password_secure = db.Column(db.String(20))

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

