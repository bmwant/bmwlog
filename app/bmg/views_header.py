import json
from bottle import request, redirect
from models import *
from gen_forms import *
from user_controller import require
from app import app, env


class PeeweeModelEncoder(json.JSONEncoder):
    def default(self, o):
        return o._data