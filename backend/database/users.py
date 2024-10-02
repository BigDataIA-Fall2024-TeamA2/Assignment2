from datetime import datetime

from sqlalchemy import Boolean, Column, Float, String, Integer, DateTime

from backend.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(name="id", type_=Integer, primary_key=True, autoincrement=True,)
    username = Column(name="username", type_=String, unique=True, index=True)
    password = Column(name="password", type_=String)
    email = Column(name="email", type_=String)
    full_name = Column(name="first_name", type_=String, nullable=True)
    active = Column(name="active", type_=Boolean)
    pwd_last_modified_at = Column(name="password_modified_timestamp", type_=DateTime)
    created_at = Column(name="created_at", type_=DateTime, default=datetime.now())
    modified_at = Column(name="modified_at", type_=DateTime, default=datetime.now(), onupdate=datetime.now())
