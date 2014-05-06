from bottle import Bottle
from flash import FlashPlugin
from beaker.middleware import SessionMiddleware
from jinja2 import Environment, PackageLoader


app = Bottle()
app.install(FlashPlugin(secret='secreto'))


env = Environment(loader=PackageLoader('app', '../templates'))
env.globals['app'] = app

from app.views import *




