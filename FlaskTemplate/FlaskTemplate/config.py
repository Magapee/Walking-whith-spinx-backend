import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    #-------------------------------------------Flask
    SECRET_KEY = os.urandom(2**10)
    #-------------------------------------------flask-mail
    
    MAIL_SERVER = 'smtp.mail.ru'
    MAIL_PORT  = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'gay_egor@mail.ru'
    MAIL_PASSWORD = 'Gaygaygay123'
    MAIL_DEFAULT_SENDER = 'gay_egor@mail.ru'

    #-------------------------------------------SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    pass