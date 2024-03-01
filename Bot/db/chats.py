from Bot.db import SESSION, BASE
from sqlalchemy import Column, String, Integer, UnicodeText, Boolean, func, distinct, desc

class Chats(BASE):

    __tablename__ = "chats"

    chat_id = Column(Integer, primary_key=True)
    
    def __init__(self, chat_id):
        self.chat_id = chat_id

    def __repr__(self):
        return "<Chat {}>".format(self.chat_id)
    
Chats.__table__.create(checkfirst=True)

def add_chat(chat_id):
    try:
        chat = SESSION.query(Chats).get(chat_id)
        if not chat:
            chat = Chats(chat_id)
            SESSION.add(chat)
            SESSION.commit()
            return True
    finally:
        SESSION.close()

def get_chat(chat_id):
    return SESSION.query(Chats).get(chat_id)

def get_all_chats():
    return SESSION.query(Chats).all()