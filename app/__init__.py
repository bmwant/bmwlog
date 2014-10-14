from bottle import Bottle, Jinja2Template
from jinja2 import Environment, PackageLoader
from peewee import MySQLDatabase
import sys
import platform

if platform.system() == 'Windows':  # or 'FreeBSD' on production
    from config import DevelopmentConfig as config
else:
    from config import ProductionConfig as config


db = MySQLDatabase(config.DB_NAME,
    host=config.DB_HOST, port=config.DB_PORT,
    user=config.DB_USER, password=config.DB_PASS)

app = Bottle()

from .flash import FlashPlugin
app.install(FlashPlugin(secret=config.SECRET_KEY))

from .login_manager import LoginManager
app.install(LoginManager(secret=config.SECRET_KEY))

from .logging_plugin import LoggingPlugin
app.install(LoggingPlugin())

env = Environment(loader=PackageLoader('app', '../templates'))
env.globals['app'] = app

#if you want to add some views - import them in views.py
from app.views import *




