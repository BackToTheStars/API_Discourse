"""

import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY, gameName text, turns text)"
cursor.execute(create_table)

# cursor.execute("INSERT INTO games VALUES (1, 'Dasein', '1 - Martin Heidegger - Being and Time')")

connection.commit()
connection.close()


"""