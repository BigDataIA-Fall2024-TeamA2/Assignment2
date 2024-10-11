from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from backend.database import Base


class ChatHistory(Base):
    __tablename__ = 'chat_history'

    chat_id = Column(name="id", type_=Integer)
    question = Column(name="question", type_=String)
    answer = Column(name="answer", type_=String)
    created_at = Column(name="created_at", type_=DateTime, default=datetime.now)
