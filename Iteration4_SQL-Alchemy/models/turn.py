from db import db

class TurnModel(db.Model):
  __tablename__ = 'turns'

  id = db.Column(db.Integer, primary_key=True)                      # |
  turnName = db.Column(db.String(255))                              # |
  game_id = db.Column(db.Integer, db.ForeignKey('games.id'))        # |
                                                   # ссылка на таблицу games, столбец id 
  game = db.relationship('GameModel')                               # |
# games = db.relationship('GameModel', lazy='dynamic')              # |

  def __init__(self, turnName, game_id):                            # |
    self.turnName = turnName
    self.game_id = game_id                                          # |        

  def json(self):
#   return {'turnName': self.turnName, 'games': [game.json() for game in self.games.all()]} # added in GameModel
    return {'game_id': self.game_id, 'id': self.id, 'turnName': self.turnName}     # |

  @classmethod                                    
  def find_by_name(cls, turnName):
    return cls.query.filter_by(turnName=turnName).first()

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()