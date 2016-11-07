from main import app
from security import login_required, get_oauth_token

from flask import render_template

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'

    oauth_token = get_oauth_token()
    if oauth_token:
        response.headers['Authorization'] = oauth_token
    return response

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/dialog-team')
def dialog_team():
    return render_template('dialog-team.html')
