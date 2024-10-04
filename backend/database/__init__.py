import logging
from typing import AsyncGenerator, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from backend.config import settings

logger = logging.getLogger(__name__)

engine = create_async_engine(f"postgresql+asyncpg://{settings.POSTGRES_URI}", connect_args={"statement_cache_size": 0})
SessionLocal = async_sessionmaker(bind=engine)
Base = declarative_base()


async def db_session() -> AsyncGenerator[AsyncSession, Any]:
    _session = SessionLocal()
    try:
        yield _session
    except Exception as e:
        await _session.rollback()
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


async def _create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("[Database] All tables created")
