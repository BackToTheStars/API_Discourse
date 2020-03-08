
import sqlite3

class GameModel:
  TABLE_NAME = 'games'

  def __init__(self, id, name, turns):
    self.id = id
    self.name = name
    self.turns = turns

  def json(self):
    return {'id': self.id, 'name': self.name, 'turns': self.turns}

  @classmethod                                # скопировали из GET
  def find_by_name(cls, name):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "SELECT * FROM {table} WHERE gameName=?".format(table=cls.TABLE_NAME)
    result = cursor.execute(query, (name,))
    row = result.fetchone()
    connection.close()

    if row:
      return cls(*row)                        # cls(row[0], row[1], row[2])

  def insert(self):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "INSERT INTO {table} VALUES (?, ?, ?)".format(table=self.TABLE_NAME)
    cursor.execute(query, (self.id, self.name, self.turns))
    connection.commit()
    connection.close()

  def update(self): # получает словарь игры, где есть имя и ходы
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "UPDATE {table} SET turns=? WHERE gameName=?".format(table=self.TABLE_NAME)  # UPDATE одну строку
    cursor.execute(query, (self.turns, self.name))
    connection.commit()
    connection.close()

