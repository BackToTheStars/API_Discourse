
from db import db

class GameModel(db.Model):
  __tablename__ = 'games'

  id = db.Column(db.Integer, primary_key=True)
  gameName = db.Column(db.String(255))
  turns = db.Column(db.String(255))           # db.Float(precision=2)

  def __init__(self, id, gameName, turns):
    self.id = id
    self.gameName = gameName
    self.turns = turns

  def json(self):
    return {'id': self.id, 'gameName': self.gameName, 'turns': self.turns}

  @classmethod                                    
  def find_by_name(cls, gameName):
    return cls.query.filter_by(gameName=gameName).first()

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()
