
from user import User

users = [                           # table of users
  User(1, 'bob', 'abcd')
]

username_mapping = {u.username: u for u in users}

userid_mapping = { 1: 
  {
    'id': 1,
    'username': 'bob',
    'password': 'abcd'
  }
}

def authenticate(username, password):
  user = username_mapping.get(username, None)
  if user and user.password == password:
    return username

def identity(payload):
  user_id = payload['identity']
  return userid_mapping.get(user_id, None)