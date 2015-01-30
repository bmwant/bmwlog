__author__ = 'Most Wanted'


class Config(object):
    SECRET_KEY = 'some-secret-key'
    DB_NAME = 'bmwlog'
    DB_USER = 'bmwant21'
    DB_PASS = 'try-to-forget'
    DEBUG = True
    RELOADER = True


class LocalConfig(Config):
    DB_HOST = '127.0.0.1'
    DB_PORT = 3306
    STATIC_FOLDER = 'D:/coding/bmwlog/'
    ROOT_FOLDER = 'D:/coding/bmwlog/'
    RUN_HOST = '127.0.0.1'
    RUN_PORT = 8081
    DB_USER = 'root'
    DB_PASS = ''


class DevelopmentConfig(Config):
    DB_HOST = '94.45.76.62'
    DB_PORT = 3306
    STATIC_FOLDER = 'D:/coding/bmwlog/'
    ROOT_FOLDER = 'D:/coding/bmwlog/'
    RUN_HOST = '127.0.0.1'
    RUN_PORT = 8081


class ProductionConfig(Config):
    DB_HOST = '127.0.0.1'  # or '94.45.87.159'
    DB_PORT = 3306
    STATIC_FOLDER = '/data/projects/bmwlog/'
    ROOT_FOLDER = '/data/projects/bmwlog/'
    RUN_HOST = '0.0.0.0'
    RUN_PORT = 8031
    DEBUG = True
    RELOADER = True
