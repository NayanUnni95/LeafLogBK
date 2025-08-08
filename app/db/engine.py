from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings

engine = create_async_engine(
    str(settings.SQL_DATABASE_URI),
    pool_size=10,
    max_overflow=100,
    pool_recycle=1800,
    pool_timeout=20,
)