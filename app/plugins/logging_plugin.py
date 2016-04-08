# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
import os
import logging
import traceback


class LoggingPlugin(object):
    """
    Allows to write log for bottle applications
    """
    name = 'logging_plugin'
    api = 2
    date_format = '%H:%M:%S %d/%m/%y'
    message_format = ('%(asctime)s :: %(mod_name)s, line %(mod_line)d :: '
                      '[%(levelname)s] %(message)s')

    def __init__(self):
        # todo: add stream and format parameters
        self.app = None
        self.logger = None

    def setup(self, app):
        self.app = app
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(self.message_format)
        formatter.datefmt = self.date_format
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.logger = logger
        self.app.log = self.log

    def log(self, msg, level=None):
        tb = traceback.extract_stack(limit=2)
        mod_name = os.path.basename(tb[0][0])
        lineno = tb[0][1]
        levels = {
            'critical': 50,
            'error': 40,
            'warning': 30,
            'info': 20,
            'debug': 10,
        }
        cur_level = levels.get(level, 20)
        self.logger.log(cur_level, msg, extra={'mod_name': mod_name,
                                               'mod_line': lineno})

    def apply(self, callback, route):
        return callback
