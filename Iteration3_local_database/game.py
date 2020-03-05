
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

  @classmethod
  def insert(cls, game):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "INSERT INTO games VALUES (?, ?)"
    cursor.execute(query, (game['gameName'], game['turns']))
    connection.commit()
    connection.close()

  @classmethod
  def update(cls, game): # получает словарь игры, где есть имя и ходы
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "UPDATE games SET turns=? WHERE gameName=?"  # UPDATE одну строку
    cursor.execute(query, (game['turns'], game['gameName']))
    connection.commit()
    connection.close()

  def post(self, name):
    if self.find_by_name(name):
      return {'message': "An item with name '{}' already exists".format(name)}, 400  # bad request. Error-first approach
    data = Game.parser.parse_args()
    game = {'gameId': data['gameId'], 'gameName': name, 'turns': data['turns']} # create JSON    
    try:
      self.insert(game)
    except:
      {'message': 'Some error occurred while inserting the game'}, 500 # Internal Server Error
    return game, 201

  def put(self, name):
    data = Game.parser.parse_args()
    game = self.find_by_name(name)
    updated_game = {'id': data['gameId'], 'gameName': name, 'turns': data['turns']}
    if game is None:
      try:
        self.insert(updated_game)
      except:
        return {"message": "Error occurred inserting the game"}, 500
    else:
      try:  
        self.update(updated_game)
      except:
        return {"message": "Error occurred updating the game"}, 500
    return updated_game

  def delete(self, name):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "DELETE FROM games WHERE gameName=?"  # delete только одну строку
    cursor.execute(query, (name,))
    connection.commit()
    connection.close()
    return {'message': 'Game deleted'}


class GameList(Resource):
  def get(self):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "SELECT * FROM games"  # delete только одну строку
    result = cursor.execute(query)
    games = []
    for row in result:
      games.append({'id': row[0], 'gameName': row[1], 'turns': row[2]})
    connection.close()
    return {'games': games}
