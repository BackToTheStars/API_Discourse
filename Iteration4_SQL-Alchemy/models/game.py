
import sqlite3
from db import db

class GameModel(db.Model):
  __tablename__ = 'games'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255))
  turns = db.Column(db.String(255))           # db.Float(precision=2)

  def __init__(self, id, name, turns):
    self.id = id
    self.name = name
    self.turns = turns

  def json(self):
    return {'id': self.id, 'name': self.name, 'turns': self.turns}

  @classmethod                                    
  def find_by_name(cls, name):
    return cls.query.filter_by(name=name).first()

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self): # получает словарь игры, где есть имя и ходы
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "UPDATE {table} SET turns=? WHERE gameName=?".format(table=self.TABLE_NAME)  # UPDATE одну строку
    cursor.execute(query, (self.turns, self.name))
    connection.commit()
    connection.close()

