from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from backend.database import Base


class ChatSession(Base):
    __tablename__ = 'chat_session'

    chat_id = Column(name="id", type_=Integer, primary_key=True, autoincrement=True)
    user_id = Column(name='user_id', type_=Integer)
    pdf_extractions_id = Column(name='pdf_extractions_id', type_=Integer)
    created_at = Column(name='created_at', type_=DateTime, default=datetime.now())
