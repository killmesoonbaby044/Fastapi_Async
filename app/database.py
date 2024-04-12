from loguru import logger
from sqlalchemy.exc import InterfaceError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.config import settings_local, settings_ad

database_hostname = settings_ad.database_hostname
database_password = settings_ad.database_password
database_name = settings_ad.database_name
database_username = settings_ad.database_username

# database_hostname = settings_local.database_hostname
# database_password = settings_local.database_password
# database_name = settings_local.database_name
# database_username = settings_local.database_username

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{database_username}:{database_password}@"
    f"{database_hostname}/{database_name}"
)

# SQLALCHEMY_DATABASE_URL_sync = (
#     f"postgresql://{database_username}:{database_password}@"
#     f"{database_hostname}/{database_name}"
# )
# engine_sync = create_engine(SQLALCHEMY_DATABASE_URL_sync, echo=True)
# Session = sessionmaker(autocommit=False, autoflush=False, bind=engine_sync)

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
