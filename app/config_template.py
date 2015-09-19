__author__ = 'Most Wanted'


class Config(object):
    """
    Shared properties for all configurations. Feel free
    to override some of them in inherited class
    """
    SECRET_KEY = 'some-secret-key'
    DEBUG = True
    RELOADER = True
    POSTS_PER_PAGE = 10


class SpecificConfig(Config):
    DB_HOST = '127.0.0.1'
    DB_PORT = 3306
    STATIC_FOLDER = '/path/to/static'
    ROOT_FOLDER = '/root/folder/of/project'
    RUN_HOST = '127.0.0.1'
    RUN_PORT = 8081
    DB_USER = 'root'
    DB_PASS = ''
    DB_NAME = 'bmwlog'

