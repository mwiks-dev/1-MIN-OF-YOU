from . import db

class Pitch:

    all_pitches = []

    def __init__(self,pCategory,context,uploadedBy):
        self.pCategory = pCategory
        self.context = context
        self.uploadedBy = uploadedBy

    def save_pitch(self):
        Pitch.all_pitches.append(self)

    @classmethod
    def clear_pitches(cls):
        Pitch.all_pitches.clear()

class Comment:

    all_comments = []
    def __init__(self,pitch_id,title,content,by):
        self.pitch_id = pitch_id
        self.title = title
        self.content = content
        self.by = by

    def save_comment(self):
        Comment.all_comments.append(self)

    @classmethod
    def clear_comments(cls):
        Comment.all_comments.clear()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))

    def __repr__(self):
        return f'User {self.username}'

