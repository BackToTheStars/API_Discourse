
import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.game import GameModel


class Game(Resource):
  TABLE_NAME = 'games'

  parser = reqparse.RequestParser()
  parser.add_argument('id', type=int, required=True)
  parser.add_argument('gameName', type=str)
  parser.add_argument('turns', type=str, required=True)

  @jwt_required() 
  def get(self, name):
    game = GameModel.find_by_name(name)
    if game:
      return game.json()
    return {'message': 'Game not found'}, 404

  def post(self, name):
    status = 'failure'
    if GameModel.find_by_name(name):
      return {'message': "An item with name '{}' already exists".format(name)}, 400  # bad request. Error-first approach

    data = Game.parser.parse_args()
    game = GameModel(data['id'], name, data['turns'])    
    try:
      game.insert()
      status = 'success, game created'
    except:
      {'status': status, 'message': 'Some error occurred while inserting the game'}, 500 # Internal Server Error
    return {"game": game.json(), "status": status}, 201

  def put(self, name):
    status = 'failure'
    data = Game.parser.parse_args()
    game = GameModel.find_by_name(name)
    updated_game = GameModel(data['id'], name, data['turns'])
    if game is None:
      try:
        updated_game.insert()
        status = 'success, inserted'
      except:
        return {"status": status, "message": "Error occurred inserting the game"}, 500
    else:
      try:  
        updated_game.update()
        status = 'success, updated'
      except:
        return {"message": "Error occurred updating the game"}, 500
    return {"status": status, "game": updated_game.json()}

  def delete(self, name):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "DELETE FROM {table} WHERE gameName=?".format(table=self.TABLE_NAME)  # delete только одну строку
    cursor.execute(query, (name,))
    connection.commit()
    connection.close()
    return {'message': 'Game deleted'}


class GameList(Resource):
  TABLE_NAME = 'games'
  
  @jwt_required() 
  def get(self):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)  # delete только одну строку
    result = cursor.execute(query)
    games = []
    for row in result:
      games.append({'id': row[0], 'gameName': row[1], 'turns': row[2]})
    connection.close()
    return {'games': games}
