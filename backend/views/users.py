from fastapi import APIRouter, status, HTTPException

from backend.database.users import UserModel
from backend.schemas import ExceptionSchema
from backend.schemas.users import UserRequest, UserResponse
from backend.services.users import _create_user

users_router = APIRouter(prefix="/users")


@users_router.post(
    "/",
    response_model=UserResponse,
    responses={status.HTTP_409_CONFLICT: {"model": ExceptionSchema}},
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user: UserRequest) -> UserModel:
    if created_user := await _create_user(user=user):
        return created_user
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"UserModel `{user.username}` already exists",
    )


@users_router.get(
    "/",
    response_model=UserResponse,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema}},
)
async def get_user(user) -> UserResponse:
    return await ...
