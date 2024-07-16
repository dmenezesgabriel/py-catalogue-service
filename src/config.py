import logging
import logging.config
import os
from typing import Optional

from src.port.parameter_store import ParameterStore
from src.utils.singleton import Singleton


class Config(metaclass=Singleton):
    ENVIRONMENT = "local"
    LOG_LEVEL = "DEBUG"
    QUEUE_NAME = os.getenv("QUEUE_NAME", "product-update")
    ENDPOINT_URL = os.getenv("ENDPOINT_URL")
    REGION_NAME = os.getenv("REGION_NAME", "us-east-1")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    def __init__(self, parameter_store: Optional[ParameterStore] = None):
        self._parameter_store = parameter_store

    def set_parameter_store(self, parameter_store):
        self._parameter_store = parameter_store

    def get_database_url(self):
        return self._parameter_store.get_database_url()


class LocalConfig(Config):
    pass


class TestConfig(Config):
    ENVIRONMENT = "test"


class DevelopmentConfig(Config):
    ENVIRONMENT = "development"


class StagingConfig(Config):
    ENVIRONMENT = "staging"
    LOG_LEVEL = "INFO"


class ProductionConfig(Config):
    ENVIRONMENT = "production"
    LOG_LEVEL = "INFO"


def config_factory(environment: str) -> Config:
    configs = {
        "local": LocalConfig,
        "test": TestConfig,
        "development": DevelopmentConfig,
        "staging": StagingConfig,
        "production": ProductionConfig,
    }
    config_class = configs[environment]
    return config_class()


def get_config() -> Config:
    environment = os.getenv("ENVIRONMENT", "local")
    app_config = config_factory(environment)

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "standard": {
                "format": (
                    "[%(asctime)s] %(levelname)s "
                    "[%(filename)s.%(funcName)s:%(lineno)d] "
                    "%(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "stdout_logger": {
                "formatter": "standard",
                "class": "logging.StreamHandler",
            }
        },
        "loggers": {
            "app": {
                "level": app_config.LOG_LEVEL,
                "handlers": ["stdout_logger"],
                "propagate": False,
            }
        },
    }
    logging.config.dictConfig(LOGGING)
    return app_config
