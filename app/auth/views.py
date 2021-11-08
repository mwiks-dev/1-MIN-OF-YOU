from . import auth
from flask_login import login_user,login_required,logout_user
from flask import render_template,url_for,flash,redirect,request
from .forms import SignupForm,SigninForm
from ..models import User
from .. import db
from ..email import mail_message

@auth.route('/signup', methods = ["GET","POST"])
def signup():
  signupform = SignupForm()
  if signupform.validate_on_submit():
    user = User(email = signupform.email.data, username = signupform.username.data, password = signupform.password.data)
    user.save_u()
    mail_message("Welcome to 1 Min Of You","email/welcome_user",user.email,user=user)
    return redirect(url_for('auth.signin'))
  return render_template('auth/signup.html', signupform = signupform)


@auth.route('/signin', methods = ['GET','POST'])
def signin():
  signinform = SigninForm()
  if signinform.validate_on_submit():
    user = User.query.filter_by(email = signinform.email.data).first()
    if user is not None and user.verify_password(signinform.password.data):
      login_user(user,signinform.remember_me.data)
      return redirect(request.args.get('next') or url_for('main.index'))

    flash('Invalid username or Password')
  title = "1 Min Of You Login"
  return render_template('auth/signin.html', signinform=signinform,title=title)


@auth.route('/signout')
@login_required
def signout():
  logout_user()
  return redirect(url_for("auth.signin"))