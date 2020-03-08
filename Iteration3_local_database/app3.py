
# Задачи:

# 1. API для загрузки новости/текста/автора/даты для дальнейшего анализа
# 2. API для загрузки видео/трансформации в текст


from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from user import UserRegister
from game import Game, GameList

app = Flask(__name__)
app.secret_key = 'app'                          # should be long and secure
api = Api(app)

jwt = JWT(app, authenticate, identity)          # creates new endpoint /auth


api.add_resource(Game, '/game/<string:name>')    # GET http://127.0.0.1:5000/game/Proton
api.add_resource(GameList, '/games')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':        # запускаем только если этот файл запущен как главный
  app.run(port=5000, debug=True)


