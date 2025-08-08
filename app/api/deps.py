from typing import Annotated
from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.engine import engine
from app.util.security import JWTUtils


async def get_db() -> AsyncGenerator:
    async with AsyncSession(engine) as session:
        try:
            yield session
        finally:
            await session.close()


SessionDep = Annotated[AsyncSession, Depends(get_db)]
CurrentUserDep = Annotated[dict, Depends(JWTUtils.get_current_user)]