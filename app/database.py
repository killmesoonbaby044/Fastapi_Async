from loguru import logger
from sqlalchemy.exc import InterfaceError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from .config import settings_local as settings

db_hostname = settings.database_hostname
db_password = settings.database_password
db_name = settings.database_name
db_username = settings.database_username

# database_hostname = settings_local.database_hostname
# database_password = settings_local.database_password
# database_name = settings_local.database_name
# database_username = settings_local.database_username
Base = declarative_base()

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{db_username}:{db_password}@" f"{db_hostname}/{db_name}"
)

# FOR ALEMBIC
SQLALCHEMY_DATABASE_URL_sync = (
    f"postgresql://{db_username}:{db_password}@" f"{db_hostname}/{db_name}"
)
# engine_sync = create_engine(SQLALCHEMY_DATABASE_URL_sync, echo=True)
# Session = sessionmaker(autocommit=False, autoflush=False, bind=engine_sync)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
Session_async = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_async_db():
    async with Session_async() as session:
        try:
            yield session
        except (ConnectionRefusedError, InterfaceError) as e:
            logger.bind(file="sql").error(f"NO CONNECTION TO DB -->> {e!r}")
        # except Exception as e:
        #     logger.bind(file="sql").error(f"NO CONNECTION TO DB -->> {str(e)}")
