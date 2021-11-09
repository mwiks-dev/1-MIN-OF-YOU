from flask import render_template,redirect,url_for,abort,request
from flask_login.utils import login_required,current_user
from . import main
from ..models import Comment,Pitch, User
from .forms import CommentForm, PitchForm,UpdateProfile
from .. import db,photos
import markdown2

# Views
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    title = '1MinOfYou'
    pitches = Pitch.query.all()
    pickuplines = Pitch.query.filter_by(category = 'Pick-up Lines').all()
    sales = Pitch.query.filter_by(category = 'Sales').all()
    innovation = Pitch.query.filter_by(category = 'Innovation').all()
    humanity = Pitch.query.filter_by(category = 'Humanity').all()
    music = Pitch.query.filter_by(category = 'Music').all()
    religion = Pitch.query.filter_by(category = 'Religion').all()

    return render_template('index.html',title = title,pitches = pitches,pickuplines=pickuplines,sales=sales,innovation=innovation,humanity=humanity,music=music,religion=religion)

@main.route('/user/<name>')
def profile(name):
    user = User.query.filter_by(username = name).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<name>/update',methods = ['GET','POST'])
@login_required
def update_profile(name):
    user = User.query.filter_by(username = name).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',name = user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<name>/update/pic',methods= ['POST'])
@login_required
def update_pic(name):
    user = User.query.filter_by(username = name).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.avatar = path
        db.session.commit()
    return redirect(url_for('main.profile',name = name))

@main.route('/create_new',methods = ['GET','POST'])
@login_required
def new_pitch():
    form = PitchForm()

    if form.validate_on_submit():
        category = form.category.data
        context = form.context.data
        new_pitch = Pitch(category=category,context=context,user=current_user)
        #saving new pitch
        new_pitch.save_pitch()
        return redirect(url_for('main.index'))

    return render_template('pitch.html',pitch_form = form)

@main.route('/pitch/comment/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_comment(pitch_id):
    form = CommentForm()
    pitch=Pitch.query.get(pitch_id)
    all_comments = Comment.query.filter_by(pitch_id)
    if form.validate_on_submit():
        title = form.title.data
        comment = form.comment.data
        pitch_id = pitch_id
        user_id = current_user._get_current_object().id
        # Updated comment instance
        new_comment= Comment(title=title,comment=comment,user_id=user_id,pitch_id=pitch_id,comment_form=form)

        # save review method
        new_comment.save_comment()
        return redirect(url_for('.comment',pitch_id = pitch_id ))
    return render_template('new_comment.html',pitch=pitch,all_comments=all_comments)

@main.route('/comment/<int:id>')
@login_required
def single_comment(id):
    comment = Pitch.query.get(id)
    if comment is None:
        abort(404)
    format_comment = markdown2.markdown(comment.pitch_comment,extras=["code-friendly","fenced-code blocks"])
    return render_template('comment.html',comment = comment,format_comment = format_comment)
        