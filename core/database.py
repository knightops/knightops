from functools import lru_cache
from typing import Iterator

from fastapi_utils.session import FastAPISessionMaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from core.config import settings

Base = declarative_base()


def get_db() -> Iterator[Session]:
    """ FastAPI dependency that provides a sqlalchemy session """
    yield from _get_fastapi_sessionmaker().get_db()


@lru_cache()
def _get_fastapi_sessionmaker() -> FastAPISessionMaker:
    """ This function could be replaced with a global variable if preferred """
    database_uri = settings.SQLALCHEMY_DATABASE_URI
    return FastAPISessionMaker(database_uri)

