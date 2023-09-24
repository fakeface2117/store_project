from typing import Union

from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

SessionLocal: Union[sessionmaker, None] = None


async def get_db():
    async with SessionLocal() as db:
        yield db
