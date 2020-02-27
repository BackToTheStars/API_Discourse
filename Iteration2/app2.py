
from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

games = []


class Game(Resource):
  
  def get(self, name):
    for game in games:
      if game['gameName'] == name:
        return game                      
  
  def post(self, name):
    game = {
      'gameId': 1,
      'gameName': name,
      'turns': [],
    }
    games.append(game)
    return game



api.add_resource(Game, '/game/<string:name>')    # GET http://127.0.0.1:5000/game/Proton Mass



app.run(port=5000)


