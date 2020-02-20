import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """
    Base application configuration
    """
    DEBUG = False
    TESTING = False
    MONGODB_DB_NAME = 'closet_stats'
    MONGODB_DB_SERVER = os.getenv('CSTATS_DATABASE_SERVER', 'example.com')
    MONGODB_DB_USER = os.getenv('CSTATS_DATABASE_USER', 'user')
    MONGODB_DB_PASS = os.getenv('CSTATS_DATABASE_PWD', 'pass')


class DevelopmentConfig(BaseConfig):
    """
    Development application configuration
    """
    DEBUG = True
    TESTING = False


class TestingConfig(BaseConfig):
    """
    Testing application configuration
    """
    DEBUG = True
    TESTING = True


class ProductionConfig(BaseConfig):
    """
    Production application configuration
    """
    DEBUG = False
    TESTING = False
