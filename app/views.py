from flask import render_template
from app import app

# Views
@app.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = '1MinOfYou'
    message = 'Welcome to 1 Min Of You'
    return render_template('index.html',title = title,message = message)