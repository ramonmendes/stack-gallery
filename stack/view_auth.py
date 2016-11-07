from main import app
from security import login_required, login_authorized, validate_token, revoke_token

from flask import Flask, redirect, url_for, session
from flask import render_template
from flask import request, abort
from flask_oauth import OAuth


# You must configure these 3 values from Google APIs console
# https://code.google.com/apis/console
GOOGLE_CLIENT_ID = app.config['GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SECRET = app.config['GOOGLE_CLIENT_SECRET']
REDIRECT_URI = 'authorized'  # one of the Redirect URIs from Google APIs console

VALID_EMAIL_DOMAIN = '@ciandt.com'
KEY_ACCESS_TOKEN = 'access_token'

# Google URL
# https://accounts.google.com/.well-known/openid-configuration
oauth = OAuth()
google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)


@app.route('/signin')
def signin():
    return render_template('login.html')

@app.route('/login')
def login():
    print REDIRECT_URI,GOOGLE_CLIENT_ID,GOOGLE_CLIENT_SECRET
    callback=url_for(REDIRECT_URI, _external=True)
    return google.authorize(callback=callback)

@app.route('/logout')
def logout():
    access_token = session.get(KEY_ACCESS_TOKEN)
    if access_token:
      session.pop(KEY_ACCESS_TOKEN, None)
      revoke_token(access_token[0])

    return redirect(url_for('index'))

@app.route('/%s'% REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp[KEY_ACCESS_TOKEN]

    user = validate_token('OAuth %s' % access_token)
    if not VALID_EMAIL_DOMAIN in user['email']:
      print ('Unauthorized access')
      abort(403)
    else:
      print ('USER LOGGED: %s' % user['email'])
      session[KEY_ACCESS_TOKEN] = access_token, ''
      return redirect(url_for('index'))

@google.tokengetter
def get_access_token():
    return session.get(KEY_ACCESS_TOKEN)
