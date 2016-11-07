from main import app
from version import __version__
from security import login_authorized

from flask import jsonify
from flask import request
import logging
from elasticsearch import Elasticsearch

logger = logging.getLogger('stack')

config = {'elasticsearch' : app.config['ELASTICSEARCH_URL']}

@app.route('/api/version', methods = ['GET'])
def api_version():
	return jsonify(__version__)

@app.route('/api/stacks/', methods = ['GET'])
@login_authorized
def api_stack(user):
	r = Database(config)

	return jsonify(r.list_stack())

@app.route('/api/stacks/search', methods = ['GET'])
@login_authorized
def api_stack_search(user):
	q = request.args.get('q')
	r = Database(config)

	return jsonify(r.search_stack(q))

@app.route('/api/stacks/<id>', methods = ['GET'])
@login_authorized
def api_stack_id(id):
	source = request.args.get('_source')
	r = Database(config)

	return jsonify(r.get_stack(id, source))

@app.route('/api/stacks/<id>', methods = ['POST'])
@login_authorized
def api_stack_post(id):
	payload = request.json
	print (payload)

	return id, 200

@app.route('/api/stacks/team/<id>', methods = ['GET'])
@login_authorized
def api_team(user, id):
	source='team.*'
	r = Database(config)
	stack = r.get_stack(id, source)

	return jsonify(stack['_source']['team'])


class Database(object):
	def __init__(self, config):
		self.es = Elasticsearch([config['elasticsearch']])

	def save_document(self, index, document_type, document, id=None):
		res = self.es.index(index=index, doc_type=document_type, body=document, id=id)
		logger.debug("Created documento ID %s" % res['_id'])

	def search_by_query(self, index, query):
		"""
		Sample of query: {"query": {"match_all": {}}}
		"""
		resp = self.es.search(index=index, body=query, size=2500)
		logger.debug("%d documents found" % resp['hits']['total'])

		return resp

	def search_stack(self, q):
		query = {
		    "query": {
		        "query_string": {
		           "query": q
		        }
		    }
		}
		logger.debug('query %s' % query)

		data = self.search_by_query('stack', query)
		list_stack = []
		for item in data['hits']['hits']:
			list_stack.append(item['_source'])

		return list_stack


	def list_stack(self):
		index = 'stack'
		data = self.es.search(index=index, body={"query": {"match_all": {}}}, size=2500, sort='name:desc')
		list_stack = []
		for item in data['hits']['hits']:
			stack = item['_source']
			stack['like_count'] = 0
			list_stack.append(item['_source'])

		return list_stack

	def get_stack(self, id, source):
		if source:
			print source
			return self.es.get(index='stack', doc_type='setting', id=id, _source=source)
		else:
			return self.es.get(index='stack', doc_type='setting', id=id)
