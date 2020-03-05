
import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Game(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('turns', type=str, required=True)
  parser.add_argument('gameId', type=int, required=True)

  @jwt_required() 
  def get(self, name):
    game = self.find_by_name(name)
    if game:
      return game
    return {'message': 'Game not found'}, 404
    

  @classmethod                                # скопировали из GET
  def find_by_name(cls, name):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "SELECT * FROM games WHERE gameName=?"
    result = cursor.execute(query, (name,))
    row = result.fetchone()
    connection.close()
    if row:
      return {'game': {'gameId': row[0], 'gameName': row[1], 'turns': row[2]}}
  


  def post(self, name):
    if self.find_by_name(name):
      return {'message': "An item with name '{}' already exists".format(name)}, 400  # bad request. Error-first approach

    data = Game.parser.parse_args()

    game = {
      'gameId': data['gameId'],
      'gameName': name,
      'turns': data['turns']
    }
    
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "iNSERT INTO games VALUES (?, ?, ?)"
    cursor.execute(query, (game['gameId'], game['gameName'], game['turns']))
    connection.commit()
    connection.close()

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
