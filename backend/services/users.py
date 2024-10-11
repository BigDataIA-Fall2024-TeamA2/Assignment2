import logging

from sqlalchemy.exc import IntegrityError

from backend.database import db_session
from backend.database.users import UserModel
from backend.schemas.users import UserRequest, UserCreateRequest, UserResponse

logger = logging.getLogger(__name__)


async def _create_user(user: UserRequest) -> UserModel | None:
    try:
        with db_session() as session:
            _user = UserModel(**UserCreateRequest(**user.model_dump()).model_dump())
            session.add(_user)
            session.commit()
            session.refresh(_user)
            return _user
    except IntegrityError as ie:
        logger.error(f"UserModel creation failed with error {ie}")
    except Exception as e:
        logger.exception(e)
    return None
