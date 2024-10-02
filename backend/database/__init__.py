import logging
import os
from contextlib import contextmanager
from typing import AsyncGenerator, Any

from sqlalchemy import create_engine, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

from backend.config import settings

logger = logging.getLogger(__name__)

engine = create_async_engine(f"postgresql+asyncpg://{settings.POSTGRES_URI}")
SessionLocal = async_sessionmaker(bind=engine)
Base = declarative_base()


async def db_session() -> AsyncGenerator[AsyncSession, Any]:
    _session = SessionLocal()
    try:
        yield _session
    except Exception as e:
        raise ValueError(f"Failed to connect to database: {e}")
    finally:
        await _session.close()


async def database_health(db: AsyncSession) -> bool:
    """
    Health check for the database connection
    :param db:
    :return:
    """
    try:
        await db.execute(select(1))
        return True
    except Exception:
        return False
