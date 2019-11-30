import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    #-------------------------------------------Flask
    SECRET_KEY = os.urandom(2**10)

    #-------------------------------------------SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    pass