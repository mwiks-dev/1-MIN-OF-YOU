from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms import validators
from wtforms.fields.choices import SelectField
# from wtforms.validators import Required

class PitchForm(FlaskForm):
    category = SelectField('Pitch Ctaegory',choices = [('Pick-up Lines','Pick-up Lines'),('Sales','Sales'),('Innovation','Innovation'),('Humanity','Humanity'),('Music','Music'),('Tech','Tech')]) 
    context = TextAreaField('Pitch itself')
    uploadedBy = StringField('Your Name')
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    title = StringField('Comment title')
    comment = TextAreaField('Pitch comment')
    submit = SubmitField('Submit')