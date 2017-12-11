"""
Config module
"""
SECRET_KEY = 'some-secret-key'
DEBUG = True
RELOADER = True
POSTS_PER_PAGE = 10
DB_HOST = '127.0.0.1'
DB_PORT = 3306
STATIC_FOLDER = '/home/vagrant/workspace/bmwlog/static'
ROOT_FOLDER = '/home/vagrant/workspace/bmwlog'
# only applicable if will run as standalone app
RUN_HOST = '127.0.0.1'
RUN_PORT = 8031
DB_USER = 'root'
DB_PASS = ''
DB_NAME = 'bmwlogdb'
