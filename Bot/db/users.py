from Bot.db import SESSION, BASE
from sqlalchemy import Column, Integer, UnicodeText

class Users(BASE):

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(UnicodeText)
    wins = Column(Integer, default=0)
    played = Column(Integer, default=0)
    
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
        self.wins = 0
        self.played = 0

    def __repr__(self):
        return "<User {}>".format(self.user_id)
    
Users.__table__.create(checkfirst=True)

def add_user(user_id, username):
    try:
        user = SESSION.query(Users).get(user_id)
        if not user or user.username != username:
            user = Users(user_id, username)
            SESSION.add(user)
            SESSION.commit()
            return True
    finally:
        SESSION.close()
    

def id_to_username(user_id):
    try:
        user = SESSION.query(Users).get(user_id)
        if user:
            return user.username
    finally:
        SESSION.close()


def get_user(user_id):
    return SESSION.query(Users).get(user_id)

def get_all_users():
    return SESSION.query(Users).all()