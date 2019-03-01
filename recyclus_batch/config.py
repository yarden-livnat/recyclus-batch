"""Application configuration."""
from pathlib import Path

db_dir = Path('.').parent.resolve()


class Config(object):
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis"

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    DB_NAME = 'dev.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_dir / "gateway_dev.db"}'



class TestingConfig(Config):
    TESTING = True
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_dir / "gateway_test.db"}'
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False


config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)