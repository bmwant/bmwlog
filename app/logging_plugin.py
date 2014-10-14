# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
import logging
from bottle import request, response, hook


class LoggingPlugin(object):
    """
    Allows to write log for bottle applications
    """
    name = 'logging_plugin'
    api = 2

    def __init__(self):
        #todo: add stream and format parameters
        self.app = None
        self.logger = None

    def setup(self, app):
        self.app = app

        #self.app.add_hook('before_request', self.load_flashed)
        #self.app.add_hook('after_request', self.set_flashed)
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(module)s:%(asctime)s:[%(levelname)s] %(message)s')
        formatter.datefmt = '%d/%m/%y %H:%M'
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.logger = logger
        self.app.log = self.log

    def log(self, msg, level=None):
        self.logger.log(30, msg)

    def apply(self, callback, route):
        return callback
