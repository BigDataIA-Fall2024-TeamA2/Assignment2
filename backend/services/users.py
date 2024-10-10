import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from backend.database.users import User
from backend.schemas.users import UserRequest, UserCreateRequest, UserResponse

logger = logging.getLogger(__name__)


async def _create_user(user: UserRequest, db_session: Session) -> UserResponse | None:
    try:
        user = User(**UserCreateRequest(**user.model_dump()).model_dump())
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user
    except IntegrityError as ie:
        logger.error(f"User creation failed with error {ie}")
    except Exception as e:
        logger.exception(e)
    return None
