import logging

from loguru import logger

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from app.config import settings

database_hostname = settings.database_hostname
database_password = settings.database_password
database_name = settings.database_name
database_username = settings.database_username

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{database_username}:{database_password}@"
    f"{database_hostname}/{database_name}"
)
SQLALCHEMY_DATABASE_URL_sync = (
    f"postgresql://{database_username}:{database_password}@"
    f"{database_hostname}/{database_name}"
)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


Session_async = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_async_db():
    db = Session_async()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(str(e))
    finally:
        await db.close()
        print("closed\n")


engine_sync = create_engine(SQLALCHEMY_DATABASE_URL_sync, echo=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine_sync)
