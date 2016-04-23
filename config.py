import os
basedir = os.path.abspath(os.path.dirname(__file__))

"""This module manages different configurations for different environments."""


# Parse database configuration from $DATABASE_URL
class Config(object):
    """Default configurations."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository') 
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class DevelopmentConfig(Config):
    """Config for Development."""
    DEVELOPMENT = True
    DEBUG = True
    TRAP_BAD_REQUEST_ERRORS = True


class TestingConfig(Config):
    """Testing configurations."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_URL')