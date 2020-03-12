
from flask_restful import Resource
from models.school import SchoolModel

class School(Resource):
  
  def get(self, schoolName):
    school = SchoolModel.find_by_name(schoolName)
    if school:
      return school.json(), 200
    return {'message': 'School not found'}, 404


  def post(self, schoolName):
    if SchoolModel.find_by_name(schoolName):
      return {'message': 'School with name {} already exists.'.format(schoolName)}, 400
    school = SchoolModel(schoolName)
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
