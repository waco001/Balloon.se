from flask.ext.restful import reqparse, Resource, Api

class UserRegister(Resource):
	def post(self):
		parser = reqparse.RequestParser()
        parser.add_argument('phone_number', type=int, required=True)
      	parser.add_argument('provider', type=str, required=True)
      	parser.add_argument('provider', type=str, required=True)
        request_params = parser.parse_args()
        result = process_the_request(request_params)
        response = {
             'result': result,
             'error_code': 0
        }
        return response