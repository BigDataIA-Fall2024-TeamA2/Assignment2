from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.users import User
from backend.schemas.auth import Token
from backend.schemas.users import UserResponse
from backend.utils import verify_password


async def authenticate_user(username: str, password: str, db: AsyncSession) -> UserResponse | HTTPException | None:
    user = await db.scalar(select(User).filter_by(username=username))
    if user and verify_password(plain_password=password, hashed_password=user.password):
        return await validate_user(user=user)
    return None


async def validate_user(user: User) -> User | HTTPException:
    if not user.active:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your account is deactivated.")
    return user


async def generate_token(user: User) -> Token:
    ...

