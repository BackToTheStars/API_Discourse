
from flask_restful import Resource
from models.game import GameModel                                              # |

class Turn(Resource):
  
  def get(self, turnName):
    turn = TurnModel.find_by_name(turnName)
    if turn:
      return turn.json(), 200
    return {'message': 'Turn not found'}, 404


  def post(self, turnName):
    if TurnModel.find_by_name(turnName):
      return {'message': 'Turn with name {} already exists.'.format(turnName)}, 400
    turn = TurnModel(turnName)
    try:
      school.save_to_db()
    except:
      return {'message': 'An error occurred while saving the school. Database error.'}, 500
    return school.json(), 201


  def delete(self, schoolName):
    school = SchoolModel.find_by_name(schoolName)
    if school:
      school.delete_from_db() 
    return {'message': 'School deleted. Sorry to see it.'}

class SchoolList(Resource):
  def get(self):
    return {'Schools': [school.json() for school in SchoolModel.query.all()]} # or use map(lambda)