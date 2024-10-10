from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from backend.database import db_session
from backend.schemas import ExceptionSchema
from backend.schemas.auth import Token, Credentials, RefreshToken
from backend.services.auth import authenticate_user, generate_token, authenticate_refresh_token

auth_router = APIRouter(prefix="/auth")


@auth_router.post(
    "/token",
    response_model=Token,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema}}
)
async def token(credentials: Credentials, db: Session = Depends(db_session)) -> Token | HTTPException:
    if user := await authenticate_user(
            username=credentials.username,
            password=credentials.password,
            db=db
    ):
        return await generate_token(user)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")


@auth_router.post(
    "/refresh",
    response_model=Token,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema}}
)
async def refresh_token(request: RefreshToken, db: Session = Depends(db_session)) -> Token | HTTPException:
    if new_tokens := await authenticate_refresh_token(
            token=request.refresh_token, db=db
    ):
        return new_tokens
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
