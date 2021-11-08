from flask_wtf import FlaskForm
from wtforms.validators import Email,EqualTo
from ..models import User
from wtforms import ValidationError, StringField,PasswordField,SubmitField,BooleanField

class SignupForm(FlaskForm):
    email = StringField('Your Email Address',Email())
    name = StringField('Enter Your Username')
    password = PasswordField('Password', EqualTo('password_confirm',message = 'Passwords must match'))
    password_confirm = PasswordField('Confirm Passwords')
    submit = SubmitField('Create account')

    def validate_email(self,data_field):
        if User.query.filter_by(email = data_field.data).first():
            raise ValidationError("The Email has already been taken!")
    
    def validate_username(self, data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError("The username has already been taken")

class SigninForm(FlaskForm):
    email = StringField('Your Email Address',Email())
    password = PasswordField('Password')
    remember_me = BooleanField('Remember Me!')
    submit = SubmitField('Sign In')

