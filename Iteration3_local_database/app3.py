
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'app'                          # should be long and secure
api = Api(app)

jwt = JWT(app, authenticate, identity)          # creates new endpoint /auth

games = []


class Game(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('turns', type=dict, location='json', required=True)
  parser.add_argument('gameId', type=int, required=True)

  @jwt_required() 
  def get(self, name):
    """ for game in games:
        if game['gameName'] == name:
          return game   
    """    
    game = next(filter(lambda x: x['gameName'] == name, games), None)  # function, object
    return {'game': game}, 200 if game else 404
  
  def post(self, name):

    if next(filter(lambda x: x['gameName'] == name, games), None):
      return {'message': "An item with name '{}' already exists".format(name)}, 400  # bad request. Error-first approach.

    data = Game.parser.parse_args()

    game = {
      'gameId': data['gameId'],
      'gameName': name,
      'turns': [],
    }
    games.append(game)
    return game, 201
  
  def put(self, name):
    data = Game.parser.parse_args()
    
    game = next(filter(lambda x: x['gameName'] == name, games), None)
    if game is None:
      game = {
        'gameId': data['gameId'],
        'gameName': name,
        'turns': [(data['turns'])]
      }
      games.append(game)
    else:
      game['turns'].append(data['turns'])
    return game

  def delete(self, name):
    global games
    games = list(filter(lambda x: x['gameName'] != name, games))
    return {'message': 'Game deleted'}



class GameList(Resource):
  def get(self):
    return {'games': games}




api.add_resource(Game, '/game/<string:name>')    # GET http://127.0.0.1:5000/game/Proton Mass
api.add_resource(GameList, '/games')


app.run(port=5000, debug=True)


