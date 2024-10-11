# import contextlib
# from typing import Any, AsyncIterator
#
# from backend.config import settings
# from sqlalchemy.ext.asyncio import (
#     AsyncConnection,
#     AsyncSession,
#     async_sessionmaker,
#     create_async_engine,
# )
# from sqlalchemy.orm import DeclarativeBase
#
# class Base(DeclarativeBase):
#     # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession
#     __mapper_args__ = {"eager_defaults": True}
#
#
# class DatabaseSessionManager:
#     def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
#         self._engine = create_async_engine(host, **engine_kwargs)
#         self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine, expire_on_commit=False)
#
#     async def close(self):
#         if self._engine is None:
#             raise Exception("DatabaseSessionManager is not initialized")
#         await self._engine.dispose()
#
#         self._engine = None
#         self._sessionmaker = None
#
#     @contextlib.asynccontextmanager
#     async def connect(self) -> AsyncIterator[AsyncConnection]:
#         if self._engine is None:
#             raise Exception("DatabaseSessionManager is not initialized")
#
#         async with self._engine.begin() as connection:
#             try:
#                 yield connection
#             except Exception:
#                 await connection.rollback()
#                 raise
#
#     @contextlib.asynccontextmanager
#     async def session(self) -> AsyncIterator[AsyncSession]:
#         if self._sessionmaker is None:
#             raise Exception("DatabaseSessionManager is not initialized")
#
#         session = self._sessionmaker()
#         try:
#             yield session
#         except Exception:
#             await session.rollback()
#             raise
#         finally:
#             await session.close()
#
#
#     async def create_table(self, table):
#         async with self._engine.begin() as connection:
#             await connection.execute(table.metadata.create_all)
#
#     async def create_all(self):
#         async with self._engine.begin() as conn:
#             await conn.run_sync(Base.metadata.create_all)
#
#
# sessionmanager = DatabaseSessionManager(settings.POSTGRES_URI, {"echo": settings.SQL_ALCHEMY_ECHO_SQL})
#
#
# async def db_session() -> AsyncSession:
#     async with sessionmanager.session() as session:
#         yield session
#
#
#
# # async def database_health(db: AsyncSession) -> bool:
# #     """
# #     Health check for the database connection
# #     :param db:
# #     :return:
# #     """
# #     try:
# #         await db.execute(select(1))
# #         return True
# #     except Exception:
# #         return False
