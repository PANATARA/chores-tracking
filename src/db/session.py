from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import database

# create async engine for interaction with database
engine = create_async_engine(
    url=database.REAL_DATABASE_URL,
    future=True,
    echo=True,
    execution_options={"isolation_level": "REPEATABLE READ"},
)

# create session for the interaction with database
async_session = sessionmaker(
    engine, 
    expire_on_commit=False, 
    class_=AsyncSession,
    autocommit=False
)

async def get_db() -> AsyncGenerator:
    """Dependency for getting async session"""
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
