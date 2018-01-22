import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    'Base config class'
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

class ProductionConfig(BaseConfig):
    'Production specific config'
    DEBUG = False
    #SECRET_KEY = open('/path/to/secret/file').read()
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'dsql-data.sqlite')


class DevelopmentConfig(BaseConfig):
    'Development environment specific config'
    DEBUG = False
    TESTING = True
    SECRET_KEY = 'secret'
    Profile = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'dsql-data.sqlite')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

