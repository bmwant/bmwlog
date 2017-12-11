from __future__ import print_function
import sys

from bottle import Bottle, Jinja2Template
from jinja2 import Environment, PackageLoader
from peewee import MySQLDatabase


try:
    import config
except ImportError:
    print('No production config. Trying to local local settings', file=sys.stderr)
    import config_local as config


db = MySQLDatabase(config.DB_NAME,
                   host=config.DB_HOST, port=config.DB_PORT,
                   user=config.DB_USER, password=config.DB_PASS)
db.get_conn().ping(True)

app = Bottle()

from plugins.flash import FlashPlugin
from plugins.login_manager import LoginManager
from plugins.logging_plugin import LoggingPlugin

app.install(FlashPlugin(secret=config.SECRET_KEY))
app.install(LoginManager(secret=config.SECRET_KEY))
app.install(LoggingPlugin())

env = Environment(loader=PackageLoader('app', '../templates'))
env.globals['app'] = app

from app.helpers import p_count, dollars

env.filters['p_count'] = p_count
env.filters['dollars'] = dollars

# if you want to add some views - import them in views.py
from app.views import *
