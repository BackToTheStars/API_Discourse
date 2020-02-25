
from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)



class Game(Resource):
  def get(self, name):
    return {'game': name}

api.add_resource(Game, '/game/<string:name>')    # GET http://127.0.0.1:5000/game/Proton Mass



app.run(port=5000)


