from loguru import logger
from sqlalchemy.exc import InterfaceError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.config import settings

database_hostname = settings.database_hostname
database_password = settings.database_password
database_name = settings.database_name
database_username = settings.database_username

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{database_username}:{database_password}@"
    f"{database_hostname}/{database_name}"
)


# SQLALCHEMY_DATABASE_URL_sync = (
#     f"postgresql://{database_username}:{database_password}@"
#     f"{database_hostname}/{database_name}"
# )


logger.add(
    "sqlalchemy.log",
    level="INFO",
    rotation="10 MB",
    enqueue=True,
    compression="zip",
    filter=lambda record: record["extra"]["file"] == "sql",
)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

Session_async = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_async_db():
    async with Session_async() as session:
        try:
            yield session
        except (ConnectionRefusedError, InterfaceError) as e:
            logger.bind(file="sql").error(f"NO CONNECTION TO DB -->> {str(e)}")
        # except Exception as e:
        #     logger.bind(file="sql").error(f"NO CONNECTION TO DB -->> {str(e)}")



# engine_sync = create_engine(SQLALCHEMY_DATABASE_URL_sync, echo=True)
# Session = sessionmaker(autocommit=False, autoflush=False, bind=engine_sync)


