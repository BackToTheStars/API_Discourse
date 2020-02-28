
from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'app'                                 # should be long and secure
api = Api(app)

jwt = JWT(app, authenticate, identity)

games = []


class Game(Resource):
  
  def get(self, name):
    game = next(filter(lambda x: x['gameName'] == name, games), None)  # function, object
    return {'game': game}, 200 if game else 404

  """ for game in games:
        if game['gameName'] == name:
          return game   
  """        

  def post(self, name):
    if next(filter(lambda x: x['gameName'] == name, games), None):
      return {'message': "An item with name '{}' already exists".format(name)}, 400  # bad request
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


