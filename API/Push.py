from flask.ext.restful import reqparse, Resource, Api
import dataset, json, requests
from random import randint
import requests, time
from Weather import getWeatherFromCo
# connecting to a SQLite database
db = dataset.connect('sqlite:///balloons.db')
table = db.get_table('balloonUsers', primary_id='id', primary_type='Integer')

gcm = 'AIzaSyDZPfbfmNOj18B1gFypLBaoXNri4YGfMKU'
gcmurl = 'http://android.googleapis.com/gcm/send'


class BalloonPushAdd(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('platform', type=str, required=True)
		parser.add_argument('ident', type=str, required=True)
		request_params = parser.parse_args()
		result = self.process_request(request_params)
		return json.dumps(result)
	def process_request(self, request):
		inDatabase = table.find_one(ident=request['ident'])
		response = {
		'received' : True
		}
		if inDatabase == None:
			print("Added" + str(table.insert(dict(platform=request['platform'],ident=request['ident']))))
			response['message'] = "Created New Entry in User Database"
		else:
			print(str(inDatabase['id']) + "|" + str(inDatabase['ident']))
			response['message'] = "User Already in User Database"
		return response



class BalloonPushMessage(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('message', type=str, required=True)
		parser.add_argument('id', type=int, required=True)
		request_params = parser.parse_args()
		result = self.process_request(request_params)
		return json.dumps(result)
	def process_request(self, request):
		inDatabase = table.find_one(id=request['id'])
		response = {}
		if inDatabase == None:
			response['message'] = "Your selected id is not available."
		else:
			reg_ids = [str(inDatabase['ident'])]
			payload={
			'data' : {
				'message' : request['message']
			},
			'registration_ids':reg_ids
			}
			headers = {
			'Authorization' : gcm,
			'Content-Type' : 'application/json'
			}
			response= requests.post(gcmurl, data=json.dumps(payload), headers=headers).text
			print(response)
		return response
		