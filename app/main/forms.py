from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms import validators
from wtforms.fields.choices import SelectField
# from wtforms.validators import Required

class PitchForm(FlaskForm):
    category = SelectField('Pitch Category',choices = [('Pick-up Lines','Pick-up Lines'),('Sales','Sales'),('Innovation','Innovation'),('Humanity','Humanity'),('Music','Music'),('Tech','Tech')]) 
    context = TextAreaField('Pitch itself')
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    title = StringField('Comment title')
    comment = TextAreaField('Pitch comment')
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.')
    submit = SubmitField('Submit')