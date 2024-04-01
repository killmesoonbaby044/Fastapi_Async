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
            "level": "DEBUG",
            "propagate": False,
        },

    },
}
