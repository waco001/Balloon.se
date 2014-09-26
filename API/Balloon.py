from flask.ext.restful import reqparse, Resource, Api
import dataset, json
from math import cos
from random import randint
from Weather import getWeatherFromCo
from apscheduler.scheduler import Scheduler
# connecting to a SQLite database
db = dataset.connect('sqlite:///balloons.db')
table = db.get_table('balloonData', primary_id='id', primary_type='Integer')

# Start the scheduler
balloonsched = Scheduler()
balloonsched.start()

class BalloonUpdate(Resource):
    def get(self):
        return self.update_balloon_pos()
    def update_balloon_pos(self):
        res = db.query('SELECT * FROM balloonData WHERE airborn=1')
        for row in res:
            if int(row['time']) > 0:
                radius=3963.1676
                MilesPerDegreeLat = 69.04
                heading = json.loads(row['heading'])
                distance=4
                degrees=heading['wind_degrees']
                lat=float(row['latitude'])
                long=float(row['longitude'])
                lat+=0.00322
                long-=0.00311
                data = dict(id=row['id'], time = int(row['time'])-1,longitude = long, latitude = lat, heading = json.dumps(heading))
                table.update(data, ['id'])
                return "CHANGED " + " TO " + str(lat) + ", " + str(long)
            else:
                data = dict(id=row['id'], time=0, altitude=0, airborn=False)
                table.update(data, ['id'])
                return "Landed on the ground"
        else:
            return "No Airborn Balloons Currently"
class BalloonCreate(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('locLat', type=str, required=True)
        parser.add_argument('locLong', type=str, required=True)
        parser.add_argument('altitude', type=int, required=True)
        parser.add_argument('time', type=int, required=False)
        request_params = parser.parse_args()
        result = self.process_request(request_params)
        response = {
             'message': result['message'],
             'balloonid' : result['balloonid'],
             'error_code': result['error_code']
        }
        return response
    def process_request(self,request):
        if request['time'] == 0 or request['time'] == None:
            request['time'] = randint(1, 10)
        request['time'] *= 48 #Half-hours in a day
        heading = getWeatherFromCo(request['locLat'],request['locLong'])
        id = table.insert(dict(latitude=request['locLat'],location=heading['location'],longitude=request['locLong'],altitude=request['altitude'],time=request['time'], airborn=True, heading=json.dumps(heading)))
        response={}
        response['message']="Balloon Launched"
        response['balloonid']=id
        response['error_code']=0
        return response
class BalloonView(Resource):
    def get(self, balloonid):
        return self.process_request(balloonid)
    def process_request(self,balloonid):
        response = table.find_one(id=balloonid)
        if response == None:
        	response = {}
        	response['message'] = "The Balloon You Have Selected Is Not A Valid Balloon ID"
        return response