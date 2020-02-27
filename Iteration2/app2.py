
from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

games = []


class Game(Resource):
  
  def get(self, name):
    for game in games:
      if game['gameName'] == name:
        return game                      
    return {'game': None}, 404

  def post(self, name):
    data = request.get_json()
    game = {
      'gameId': data['gameId'],
      'gameName': name,
      'turns': [],
    }
    games.append(game)
    return game, 201

class GameList(Resource):
  def get(self):
    return {'games': games}



api.add_resource(Game, '/game/<string:name>')    # GET http://127.0.0.1:5000/game/Proton Mass
api.add_resource(GameList, '/games')


app.run(port=5000, debug=True)


