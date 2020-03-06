
import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Game(Resource):
  TABLE_NAME = 'games'

  parser = reqparse.RequestParser()
  parser.add_argument('id', type=int, required=True)
  parser.add_argument('gameName', type=str)
  parser.add_argument('turns', type=str, required=True)

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
    query = "SELECT * FROM {table} WHERE gameName=?".format(table=cls.TABLE_NAME)
    result = cursor.execute(query, (name,))
    row = result.fetchone()
    connection.close()

    if row:
      return {'game': {'id': row[0], 'gameName': row[1], 'turns': row[2]}}

  @classmethod
  def insert(cls, game):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "INSERT INTO {table} VALUES (?, ?, ?)".format(table=cls.TABLE_NAME)
    cursor.execute(query, (game['id'], game['gameName'], game['turns']))
    connection.commit()
    connection.close()

  @classmethod
  def update(cls, game): # получает словарь игры, где есть имя и ходы
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "UPDATE {table} SET turns=? WHERE gameName=?".format(table=cls.TABLE_NAME)  # UPDATE одну строку
    cursor.execute(query, (game['turns'], game['gameName']))
    connection.commit()
    connection.close()

  def post(self, name):
    status = 'failure'
    if self.find_by_name(name):
      return {'message': "An item with name '{}' already exists".format(name)}, 400  # bad request. Error-first approach

    data = Game.parser.parse_args()
    game = {'id': data['id'], 'gameName': name, 'turns': data['turns']} # create JSON    
    try:
      Game.insert(game)
      status = 'success, game created'
    except:
      {'status': status, 'message': 'Some error occurred while inserting the game'}, 500 # Internal Server Error
    return {"game": game, "status": status}, 201

  def put(self, name):
    status = 'failure'
    data = Game.parser.parse_args()
    game = self.find_by_name(name)
    updated_game = {'id': data['id'], 'gameName': name, 'turns': data['turns']}
    if game is None:
      try:
        self.insert(updated_game)
        status = 'success, inserted'
      except:
        return {"status": status, "message": "Error occurred inserting the game"}, 500
    else:
      try:  
        self.update(updated_game)
        status = 'success, updated'
      except:
        return {"message": "Error occurred updating the game"}, 500
    return {"status": status, "game": updated_game}

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
