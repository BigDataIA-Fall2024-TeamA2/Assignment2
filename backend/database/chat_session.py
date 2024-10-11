from datetime import datetime

from sqlalchemy import Column, Integer, DateTime

from backend.database import Base, db_session


class ChatSession(Base):
    __tablename__ = 'chat_sessions'

    chat_id = Column(name="chat_id", type_=Integer, primary_key=True, autoincrement=True)
    user_id = Column(name='user_id', type_=Integer)
    pdf_extractions_id = Column(name='pdf_extractions_id', type_=Integer)
    created_at = Column(name='created_at', type_=DateTime, default=datetime.now())


def create_db_chat_session(user_id, pdf_extractions_id):
    with db_session() as session:
        _chat_session = ChatSession(
            user_id=user_id,
            pdf_extractions_id=pdf_extractions_id
        )
        session.add(_chat_session)
        session.commit()
        session.refresh(_chat_session)
        return _chat_session


def get_chat_session(chat_id) -> ChatSession:
    with db_session() as session:
        return session.query(ChatSession).filter(ChatSession.chat_id == chat_id).first()
