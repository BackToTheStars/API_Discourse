from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.game import GameModel


class Game(Resource):
# TABLE_NAME = 'games'

  parser = reqparse.RequestParser()
# parser.add_argument('id', type=int, required=True)
# parser.add_argument('gameName', type=str, help='Include gameName')
# parser.add_argument('turns', type=str, required=True)
  parser.add_argument('school_id', type=int, required=True, help='every game needs a school_id')

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
    game = GameModel(name, data['school_id'])       # |
    try:
      game.save_to_db()
      status = 'success, game created'
    except:
      {'status': status, 'message': 'Some error occurred while inserting the game'}, 500 # Internal Server Error
    return {"game": game.json(), "status": status}, 201

  def put(self, name):
    data = Game.parser.parse_args()
    game = GameModel.find_by_name(name)
    
    if game is None:
      game = GameModel(name, data['school_id'])
    else: 
      game.school_id = data['school_id']

    game.save_to_db()
    return game.json()

  def delete(self, name):
    game = GameModel.find_by_name(name)
    if game:
      game.delete_from_db()
      return {'message': 'Game deleted'}
    return {'message': 'Game not found'}


class GameList(Resource):
  TABLE_NAME = 'games'
  
  @jwt_required() 
  def get(self):
    return {'games': [x.json() for x in GameModel.query.all()]}

#or return {'games': list(map(lambda x: x.json(), GameModel.query.all()))} - maybe a little faster
