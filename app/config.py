"""
Config module
"""
SECRET_KEY = ''

POSTS_PER_PAGE = 10

STATIC_FOLDER = '/data/projects/bmwlog/static'
ROOT_FOLDER = '/data/projects/bmwlog'

# Standalone run
RUN_HOST = '127.0.0.1'
RUN_PORT = 8031
DEBUG = False
RELOADER = False

# Database
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_USER = ''
DB_PASS = ''
DB_NAME = 'bmwlogdb'
