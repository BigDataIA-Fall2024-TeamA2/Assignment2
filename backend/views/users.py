from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import db_session
from backend.schemas import ExceptionSchema
from backend.schemas.users import UserRequest, UserResponse
from backend.services.users import _create_user

users_router = APIRouter(prefix="/users")


@users_router.post("/",
                   response_model=UserResponse,
                   responses={status.HTTP_409_CONFLICT: {"model": ExceptionSchema}},
                   status_code=status.HTTP_201_CREATED,
                   )
async def create_user(user: UserRequest, db: AsyncSession = Depends(db_session)) -> UserResponse :
    if created_user := await _create_user(user=user, db_session=db):
        return created_user
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"User `{user.username}` already exists"
    )


@users_router.get("/", response_model=UserResponse,
                  responses={status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema}})
async def get_user(user) -> UserResponse:
    return await ...
