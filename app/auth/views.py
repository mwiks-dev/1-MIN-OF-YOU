from . import auth
from flask_login import login_user,login_required,logout_user
from flask import render_template,url_for,flash,redirect,request
from .forms import SignupForm,SigninForm
from ..models import User
from .. import db
from ..email import mail_message

@auth.route('/signup', methods = ["GET","POST"])
def signup():
  form = SignupForm()
  if form.validate_on_submit():
    user = User(email = form.email.data, username = form.name.data, password = form.password.data)
    db.session.add(user)
    db.session.commit()
    mail_message("Welcome to 1 Min Of You","email/welcome_user",user.email,user=user)
    return redirect(url_for('auth.login'))
  return render_template('auth/signup.html', signup_form = form)


@auth.route('/login', methods = ['GET','POST'])
def login():
  signin_form = SigninForm()
  if signin_form.validate_on_submit():
    user = User.query.filter_by(email = signin_form.email.data).first()
    if user is not None and user.verify_password(signin_form.password.data):
      login_user(user,signin_form.remember_me.data)
      return redirect(request.args.get('next') or url_for('main.index'))

    flash('Invalid username or Password')
  title = "1 Min Of You Login"
  return render_template('auth/login.html', signin_form=signin_form,title=title)


@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for("main.index"))