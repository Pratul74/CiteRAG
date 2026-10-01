from .session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from typing import Annotated

db_dependency=Annotated[AsyncSession, Depends(get_db)]