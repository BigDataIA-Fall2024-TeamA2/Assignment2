from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from backend.database import Base, db_session


class ChatHistory(Base):
    __tablename__ = 'chat_history'

    chat_id = Column(name="id", type_=Integer)
    question = Column(name="question", type_=String)
    answer = Column(name="answer", type_=String)
    created_at = Column(name="created_at", type_=DateTime, default=datetime.now)


def create_db_chat_history(chat_id: int, question: str, answer: str):
    with db_session() as session:
        _chat_history = ChatHistory(
            chat_id, question, answer
        )
        session.add(_chat_history)
        session.commit()
        session.refresh(_chat_history)
        return _chat_history
