import os
basedir = os.path.abspath(os.path.dirname(__file__))

"""This module manages different configurations for different environments."""


# Parse database configuration from $DATABASE_URL
class Config(object):
    """Default configurations."""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    REMEMBER_COOKIE_DURATION = 600
    TRAP_BAD_REQUEST_ERRORS = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Andela2015@localhost/bucketlist'


class DevelopmentConfig(Config):
    """Config for Development."""
    DEVELOPMENT = True
    DEBUG = True


# class TestingConfig(Config):
#     """Testing configurations."""
#     TESTING = True
#     if os.getenv('TRAVIS_BUILD', None):
#         SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
#     else:
#         SQLALCHEMY_DATABASE_URI = os.environ['TEST_DATABASE_URL']
