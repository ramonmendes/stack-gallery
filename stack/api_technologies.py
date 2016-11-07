from main import app
from security import login_authorized

import requests
from flask import jsonify

@app.route('/api/technologies/<id>')
@login_authorized
def get_technology(user, id):
  url = 'https://tech-gallery.appspot.com/_ah/api/rest/v1/technology/%s' % id
  headers = {'Authorization': user['oauth_token']}
  response = requests.get(url=url, headers= headers)

  return jsonify(response.json())

@app.route('/api/technologies/')
@login_authorized
def technologies(user):
  url = 'https://tech-gallery.appspot.com/_ah/api/rest/v1/technology'
  headers = {'Authorization': user['oauth_token']}
  response = requests.get(url=url, headers= headers)

  return jsonify(response.json())
