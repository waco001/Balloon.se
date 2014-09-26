from flask import Flask
from Balloon import BalloonCreate, BalloonView, BalloonUpdate
from Push import BalloonPushAdd, BalloonPushMessage
from flask.ext.restful import Api
import dataset
app = Flask(__name__)
api = Api(app)



api.add_resource(BalloonCreate, '/balloon/create')
api.add_resource(BalloonView, '/balloon/<int:balloonid>')
api.add_resource(BalloonPushAdd, '/user/add')
api.add_resource(BalloonPushMessage, '/user/push')
api.add_resource(BalloonUpdate, '/update')

if __name__ == '__main__':
    app.run(debug=True,port=8000,host="0.0.0.0")