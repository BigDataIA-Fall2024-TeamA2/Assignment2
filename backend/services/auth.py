from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from backend.config import settings
from backend.database.users import User
from backend.schemas.auth import Token
from backend.utils import verify_password


async def authenticate_user(username: str, password: str, db: Session) -> Optional[User]:
    user = db.scalar(select(User).filter_by(username=username))
    if user and verify_password(plain_password=password, hashed_password=user.password):
        return await validate_user(user=user)
    return None


async def validate_user(user: User) -> User:
    if not user.active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your account is deactivated.")
    return user


async def generate_token(user: User) -> Token:
    _access_token = {
        "user_id": user.id,
        "password_timestamp": user.password_timestamp,
        "exp": datetime.utcnow() + timedelta(seconds=settings.JWT_ACCESS_TOKEN_EXPIRATION_SECONDS),
        "token_type": "access"
    }
    _refresh_token = _access_token.copy() | {
        "exp": datetime.utcnow() + timedelta(seconds=settings.JWT_REFRESH_TOKEN_EXPIRATION_SECONDS),
        "token_type": "refresh"
    }

    access_token, refresh_token = map(lambda x: jwt.encode(x, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM), (
        _access_token, _refresh_token
    ))
    return Token(access_token=access_token, refresh_token=refresh_token)


async def authenticate_refresh_token(token: str, db: Session) -> Token:
    ...
