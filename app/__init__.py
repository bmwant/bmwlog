from bottle import Bottle, Jinja2Template
from jinja2 import Environment, PackageLoader
from peewee import MySQLDatabase
from config import Config


db = MySQLDatabase(Config.DB_NAME,
    host=Config.DB_HOST, port=Config.DB_PORT,
    user=Config.DB_USER, password=Config.DB_PASS)

app = Bottle()

from .flash import FlashPlugin
app.install(FlashPlugin(secret=Config.SECRET_KEY))

from .login_manager import LoginManager
app.install(LoginManager(secret=Config.SECRET_KEY))

env = Environment(loader=PackageLoader('app', '../templates'))
env.globals['app'] = app

from app.views import *




