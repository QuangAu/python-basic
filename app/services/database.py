from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DbSessionManager:
    def __init__(self):
        self.engine: AsyncEngine | None = None
        self.sessionmaker: async_sessionmaker | None = None

    def init(self, connection_string: str):
        self.engine = create_async_engine(connection_string, poolclass=NullPool)
        self.sessionmaker = async_sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    async def close(self):
        if self.engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self.engine.dispose()
        self.engine = None
        self.sessionmaker = None

    @asynccontextmanager
    async def get_db_session(self) -> AsyncIterator[AsyncSession]:
        session = self.sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    @asynccontextmanager
    async def get_db_connection(self) -> AsyncIterator[AsyncConnection]:
        async with self.engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    # Used for testing
    async def create_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.drop_all)


sessionmanager = DbSessionManager()


async def get_db_context():
    async with sessionmanager.get_db_session() as session:
        yield session
