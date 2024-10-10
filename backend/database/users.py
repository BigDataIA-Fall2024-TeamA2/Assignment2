import logging
from datetime import datetime

from sqlalchemy import Boolean, Column, String, Integer, DateTime

from backend.database import Base

logger = logging.getLogger(__name__)


class User(Base):
    __tablename__ = "users"

    id = Column(name="id", type_=Integer, primary_key=True, autoincrement=True, )
    username = Column(name="username", type_=String, unique=True, index=True)
    password = Column(name="password", type_=String)
    email = Column(name="email", type_=String)
    full_name = Column(name="first_name", type_=String, nullable=True)
    active = Column(name="active", type_=Boolean)
    password_timestamp = Column(name="password_modified_timestamp", type_=DateTime)  # JWT Token expiration timestamp
    created_at = Column(name="created_at", type_=DateTime, default=datetime.now())
    modified_at = Column(name="modified_at", type_=DateTime, default=datetime.now(), onupdate=datetime.now())
