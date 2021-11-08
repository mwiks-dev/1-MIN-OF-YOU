from flask import render_template,redirect,url_for,abort
from flask_login.utils import login_required,current_user
from . import main
from ..models import Comment,Pitch, User
from .forms import CommentForm, PitchForm

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

    return render_template('index.html',title = title,pitches = pitches,pickuplines=pickuplines,sales=sales,innovation=innovation,humanity=humanity,music=music)

@main.route('/create_new',methods = ['GET','POST'])
@login_required
def new_pitch():
    form = PitchForm()

    if form.validate_on_submit():
        category = form.category.data
        context = form.context.data
        user_id = current_user._get_current_object().id
        new_pitch = Pitch(category=category,context=context,user_id=user_id)
        #saving new pitch
        new_pitch.save_pitch()
        return redirect(url_for('main.index'))

    return render_template('pitch.html',form = form)

# @main.route('/pitch/comment/new/<int:pitch_id')
# @login_required
# def new_comment(pitch_id):
#     form = CommentForm()
#     pitch = Pitch.query.get(pitch_id)
#     all_comments = Comment.query.filter_by(pitch_id).all()

#     if form.validate_on_submit():
#         title = form.title.data
#         comment = form.comment.data
#         user_id = current_user._get_current_object().id
#         new_comment = Comment(title=title,comment=comment,user_id=user_id)
#         #saving new comment
#         new_comment.save_comment()
#         return redirect(url_for('.comment',pitch_id=pitch_id))
#     return render_template('new_comment.html',form=form,pitch=pitch,all_comments=all_comments)
        