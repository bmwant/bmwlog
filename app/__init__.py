from __future__ import print_function
import os
import sys

from bottle import Bottle, Jinja2Template
from jinja2 import Environment, PackageLoader
from peewee import MySQLDatabase


def load_config():
    try:
        import config
    except ImportError:
        print('You haven\'t created config file', file=sys.stderr)
        sys.exit(1)

    run_mode = os.environ.get('BMWLOG_MODE', 'development')
    config_object = '%sConfig' % run_mode.capitalize()
    try:
        config_module = getattr(config, config_object)
    except AttributeError:
        print('Invalid config or environment variable. '
              'No such configuration: %s' % config_object,
              file=sys.stderr)
        sys.exit(1)
    return config_module


config = load_config()

db = MySQLDatabase(config.DB_NAME,
    host=config.DB_HOST, port=config.DB_PORT,
    user=config.DB_USER, password=config.DB_PASS)
db.get_conn().ping(True)

app = Bottle()

from plugins.flash import FlashPlugin
app.install(FlashPlugin(secret=config.SECRET_KEY))

from plugins.login_manager import LoginManager
app.install(LoginManager(secret=config.SECRET_KEY))

from plugins.logging_plugin import LoggingPlugin
app.install(LoggingPlugin())

env = Environment(loader=PackageLoader('app', '../templates'))
env.globals['app'] = app

from app.helpers import p_count, dollars

env.filters['p_count'] = p_count
env.filters['dollars'] = dollars

# if you want to add some views - import them in views.py
from app.views import *
