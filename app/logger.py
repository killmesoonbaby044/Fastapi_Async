import sys

from loguru import logger
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"standard": {"format": "%(asctime)s - %(levelname)s - %(message)s"}},
    "handlers": {
        "file_handler": {
            "class": "logging.FileHandler",
            "filename": "access.log",
            "formatter": "standard",
            "level": "INFO",
        },
        "file_handler_sqlalchemy": {
            "class": "logging.FileHandler",
            "filename": "sqlalchemy.log",
            "formatter": "standard",
            "level": "INFO",
        },
    },
    "loggers": {
        "uvicorn.access": {
            "handlers": ["file_handler"],
            "level": "INFO",
            "propagate": False,
        },
        "sqlalchemy.engine": {
            "handlers": ["file_handler_sqlalchemy"],
            "level": "INFO",
            "propagate": False,
        },

    },
}

logger.add(
    sys.stdout,
    level="INFO",
    filter=lambda record: record["extra"] is None,
)

logger.add(
    "response_validation.log",
    level="ERROR",
    rotation="10 MB",
    enqueue=True,
    compression="zip",
    filter=lambda record: record["extra"]["file"] == "RVE",
)

logger.add(
    "sqlalchemy.log",
    level="ERROR",
    rotation="10 MB",
    enqueue=True,
    compression="zip",
    filter=lambda record: record["extra"]["file"] == "sql",
)
