
from flask_restful import Resource, reqparse
from models.turn import TurnModel                                              # |

class Turn(Resource):
# TABLE_NAME = 'turns'

  parser = reqparse.RequestParser()  
  parser.add_argument('game_id', type=int, required=True, help='every turn needs a game id')

  def get(self, turnName):
    turn = TurnModel.find_by_name(turnName)
    if turn:
      return turn.json(), 200
    return {'message': 'Turn not found'}, 404


  def post(self, turnName):
    if TurnModel.find_by_name(turnName):
      return {'message': 'Turn with name {} already exists.'.format(turnName)}, 400
    
    data = Turn.parser.parse_args()
    turn = TurnModel(turnName, data['game_id'])
    try:
      turn.save_to_db()
    except:
      return {'message': 'An error occurred while saving the turn. Database error.'}, 500
    return turn.json(), 201

  def put(self, turnName):
    data = Turn.parser.parse_args()
    turn = TurnModel.find_by_name(turnName)
    
    if turn is None:
      turn = TurnModel(turnName, data['game_id'])
    else: 
      turn.game_id = data['game_id']
    turn.save_to_db()
    return turn.json()


  def delete(self, turnName):
    turn = TurnModel.find_by_name(turnName)
    if turn:
      turn.delete_from_db() 
    return {'message': 'Turn deleted.'}

class TurnList(Resource):
  def get(self):
    return {'turns': [turn.json() for turn in TurnModel.query.all()]} # or use map(lambda)