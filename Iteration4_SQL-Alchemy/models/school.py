
from db import db

class SchoolModel(db.Model):
  __tablename__ = 'schools'

  id = db.Column(db.Integer, primary_key=True)
  schoolName = db.Column(db.String(255))

  games = db.relationship('GameModel', lazy='dynamic')

  def __init__(self, schoolName):
    self.schoolName = schoolName

  def json(self):
    return {'schoolName': self.schoolName, 'games': [game.json() for game in self.games.all()]} # added in GameModel

  @classmethod                                    
  def find_by_name(cls, schoolName):
    return cls.query.filter_by(schoolName=schoolName).first()

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()