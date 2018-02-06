"""
Config module
"""
import os

SECRET_KEY = ''
DO_NOT_WRITE_BYTECODE = False

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


# Override values from config_local.py if exists
try:
    import config_local
    for key, value in config_local.__dict__.items():
        if key.isupper() and key in globals():
            globals()[key] = value
except ImportError:
    pass

# Override values from environment
for key, value in globals().copy().items():
    if key.isupper() and key in os.environ:
        globals()[key] = os.environ[key]
