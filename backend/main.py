import logging.config
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import settings
from backend.database import db_session
from backend.schemas import HealthSchema
from backend.views.auth import auth_router
from backend.views.chat import docs_router
from backend.views.users import users_router

# Load logging configuration from file
logging.config.fileConfig("backend/logging.conf", disable_existing_loggers=False)

logger = logging.getLogger(__name__)
logging.getLogger('passlib').setLevel(logging.ERROR)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("[FastAPI] Startup lifespan invoked")
    # await init_db()
    yield


app = FastAPI(title=settings.APP_TITLE, version=settings.APP_VERSION, lifespan=lifespan)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(docs_router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)


@app.get("/", response_model=HealthSchema, tags=["health"])
async def health_check(db: AsyncSession = Depends(db_session)):
    return {"api": True, "database": True}
