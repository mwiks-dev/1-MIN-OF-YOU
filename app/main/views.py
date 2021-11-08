from flask import render_template
from . import main
from ..models import Comment
from .forms import CommentForm

# Views
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    title = '1MinOfYou'
    return render_template('index.html',title = title)

# @app.route('/pitch/comment/new/')