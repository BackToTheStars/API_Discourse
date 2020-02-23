
from flask import Flask, jsonify

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
  return "Hello World!"

# GET /game/turn
# GET /game/turn/quotes
# GET /game/turn/comments
 
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




# GET /games
@app.route('/games')
def get_games():
  return jsonify({'games': games})




app.run(port=5000)

