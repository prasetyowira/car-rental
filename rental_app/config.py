"""
    This file handle configuration data of the flask app
"""
import os
from logging.config import dictConfig

from rental_app.tools.env import EnvConfig

env = EnvConfig("CR")
here = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
        This class handle configuration for the main app
    """

    _basedir = os.path.abspath(os.path.dirname(__file__))

    SECRET = env.string("SECRET", "not-so-secret")

    FLASK_DEBUG = env.boolean("DEBUG", False)
    UTC_OFFSET = 7

    DB_NAME = env.string("DB_NAME", "car_rental")
    DB_USER = env.string("DB_USER", "car_rental")
    DB_PASS = env.string("DB_PASS", "password")
    DB_HOST = env.string("DB_HOST", "localhost")
    DB_PORT = env.string("DB_PORT", "5432")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATETIME_FORMAT = env.string("DATETIME_FORMAT", "%A, %d %B %Y %H:%M:%S")

    LOGGING_CONFIG = {
        "version": 1,
        "formatters": {
            "simple": {"format": "%(asctime)s | %(name)s | %(levelname)s | %(message)s"}
        },
        "handlers": {
            "file_error": {
                "class": "logging.FileHandler",
                "level": "ERROR",
                "formatter": "simple",
                "filename": os.path.join(here, os.pardir, "logs", "error.log"),
            },
            "file_warning": {
                "class": "logging.FileHandler",
                "level": "WARNING",
                "formatter": "simple",
                "filename": os.path.join(here, os.pardir, "logs", "error.log"),
            },
            "file_app": {
                "class": "logging.FileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": os.path.join(here, os.pardir, "logs", "app.log"),
            },
            "file_access": {
                "class": "logging.FileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": os.path.join(here, os.pardir, "logs", "access.log"),
            },
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "simple",
            },
        },
        "loggers": {
            "app": {"handlers": ["console", "file_app"], "propagate": False},
            "error": {
                "handlers": ["console", "file_error", "file_warning"],
                "propagate": False,
            },
            "access": {"handlers": ["file_access"], "propagate": False},
            "alembic": {"level": "INFO", "handlers": ["console"], "propagate": False},
        },
        "root": {"level": "INFO", "handlers": ["console", "file_app", "file_error"]},
    }

    dictConfig(LOGGING_CONFIG)

    # Redis Configuration
    REDIS_HOST = env.string("REDIS_HOST", "127.0.0.1")
    REDIS_PORT = env.int("REDIS_PORT", 6379)
    MASTER_REDIS_DB = 1

    # Celery Configuration
    CELERY_RESULT_BACKEND = env.string(
        "CELERY_RESULT_BACKEND", "redis://localhost:6379"
    )
    CELERY_BROKER_URL = env.string("CELERY_BROKER_URL", "redis://localhost:6379")


class TestConfig(Config):
    """
        This class handle configuration for the test app
    """

    DB_TEST_PORT = env.string("DB_TEST_PORT", "5437")
    DB_TEST_PASS = env.string("DB_TEST_PASS", "password")
    DB_USER = Config.DB_USER
    DB_HOST = Config.DB_HOST
    DB_NAME = Config.DB_NAME

    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_TEST_PASS}@{DB_HOST}:{DB_TEST_PORT}/{DB_NAME}"

    # Redis Configuration
    REDIS_HOST = env.string("REDIS_HOST", "127.0.0.1")
    REDIS_PORT = env.int("REDIS_PORT", 6379)
    MASTER_REDIS_DB = 1

    # Celery Configuration
    CELERY_RESULT_BACKEND = env.string(
        "CELERY_RESULT_BACKEND", "redis://localhost:6379"
    )
    CELERY_BROKER_URL = env.string("CELERY_BROKER_URL", "redis://localhost:6379")
