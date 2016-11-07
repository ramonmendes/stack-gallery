from util import get_environ

from flask import Flask, url_for
import sys
import logging


mode = sys.argv[1] if len(sys.argv) > 1 else 'development'

app = Flask(__name__)
# Function to easily find your assets
# In your template use <link rel=stylesheet href="{{ static('filename') }}">
app.jinja_env.globals['static'] = (
    lambda filename: url_for('static', filename = filename)
)

################
#### config ####
################
# app.config.from_json('%s.json' % mode)

app.config['GOOGLE_CLIENT_SECRET'] = 'ScQBcaf-4zxLJDcGfuNo4G-7'
app.config['GOOGLE_CLIENT_ID'] = '596664547229-222pk998h0ihicb6v508av5pkadksisj.apps.googleusercontent.com'
app.config['ELASTICSEARCH_URL'] = 'http://104.197.92.45:9200'
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'ScQBcaf-4zxLJDcGfuNo4G-7'

########################
#### logging config ####
########################
if (2, 7) <= sys.version_info < (3, 2):
	# On Python 2.7 and Python3 < 3.2, install no-op handler to silence
	# `No handlers could be found for logger "elasticsearch"` message per
	# <https://docs.python.org/2/howto/logging.html#configuring-logging-for-a-library>
	FORMAT = '%(name)s %(levelname)-5s %(message)s'
	logging.basicConfig(format=FORMAT)
	#for item in app.config['LOGGER']:
	#	logging.getLogger(item['NAME']).setLevel(int(item['LEVELNO']))

logger = logging.getLogger('stack')
logger.info('starting app => %s ' % id(app))
logger.info('starting mode => %s ' % mode)


##############
#### view ####
##############
import view_stack
import view_auth

##############
#### APIs ####
##############
import api_stacks
import api_users
import api_technologies
import api_trends
