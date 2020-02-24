
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

games = [
          {
            'gameId': 0,                # одновременно идёт много игр
            'gameName': '',             # имя игры будет меняться от хода к ходу
            'turns': [                  # игроки делают последовательные ходы
              {
                'turnId': 0,            # номер хода в игре 
                'player': '',           # игрок, который сделал этот ход
                'dateTime': '',         # дата и время хода игрока
                'openingComment': '',   # общий открывающий комментарий хода
                'mainText': '',         # основной текст хода
                'link': '',             # http-ссылка на источник текста
                'linkDateTime': '',     # дата и время публикации оригинала в ссылке
                'quotes': [],           # цитаты
                'comments': [],         # комментарии к цитатам
                'closingComment': '',   # общий закрывающий комментарий хода
              }
            ],
          }
        ]  


@app.route('/')
def home():
  return render_template('index.html')

# GET /games                          - вывести весь список игр
# GET /game/<string:name>             - вывести игру по имени http://127.0.0.1:5000//game/some_name
# GET /game/<string:name>/turns       - вывести ходы игры по её имени
# GET /game/turn/quotes
# GET /game/turn/comments

# POST /game data: {name:}                       - создать игру 
# POST /game/<string:name>/turn/<string:number>  - создать ход игры по её имени, передать номер хода и игрока
# POST /game/turn<string:name>/text
# POST /game/turn/quotes
# POST /game/turn/comments

# DELETE /game/turn
# DELETE /game/turn/comment



# POST games/game/turn<string:name>/text
@app.route('/games/game<string:game>/turn<string:turn>/text', methods=['POST'])
def postGameTurnText(game, turn):
  pass

# POST games/game<string:game>/turn<string:turn>/quotes
@app.route('/games/game<string:game>/turn<string:turn>/quotes', methods=['POST'])
def postGameTurnQuotes(game, turn):
  pass

# GET games/game/turn<string:name>/quotes
@app.route('/games/game<string:game>/turn<string:turn>/quotes')
def getGameTurnQuotes(game, turn):
  pass





# GET /games                          - вывести весь список игр
@app.route('/games')
def get_games():
  return jsonify({'games': games})

# GET /game/<string:name>             - вывести игру по имени http://127.0.0.1:5000//game/some_name
@app.route('/game/<string:name>')
def get_game(name):
  for game in games:                  # iterate over all games
    if game['gameName'] == name:      # if the game name matches, return it
      return jsonify(game)            # if none matches, return an error message
  return jsonify({'message': 'Game not found'})

# GET /game/<string:name>/turns       - вывести ходы игры по её имени
@app.route('/game/<string:name>/turns')
def get_game_turns(name):
  for game in games:
    if game['gameName'] == name:
      return jsonify({'turns': game['turns']})
  return jsonify({'message': 'Game not found'})
  


# POST /game data: {name:}            - создать игру 
@app.route('/game', methods=['POST'])
def create_game(name):
  request_data = request.get_json()
  new_game = {
    'gameName': request_data['name'],
    'turns': []
  }
  games.append(new_game)
  return jsonify(new_game)

# POST /game/<string:name>/turn/<string:number>  - создать ход игры по её имени, передать номер хода и игрока
@app.route('/game/<string:name>/turn/<string:number>', methods=['POST'])
def create_game_turn(name, number, player):
  request_data = request.get_json()
  for game in games:
    if game['gameName'] == name:
      new_turn = {
        'turnId': request_data['number'],
        'player': request_data['player']
      }
      game['turns'].append(new_turn)
      return jsonify(new_turn)
  return jsonify({'message': 'Game not found'})


app.run(port=5000)

