# -*- coding: utf-8 -*-
import os
import logging
import traceback
from functools import partial


class LoggingPlugin(object):
    """
    Allows to write log for bottle applications
    """
    name = 'logging_plugin'
    api = 2
    date_format = '%H:%M:%S %d/%m/%y'
    message_format = ('%(asctime)s :: %(mod_name)s, line %(mod_line)d :: '
                      '[%(levelname)s] %(message)s')

    def __init__(self, level=logging.DEBUG):
        # todo: add stream and format parameters
        self.app = None
        self.logger = None
        self.level = level

    def setup(self, app):
        self.app = app
        logger = logging.getLogger(__name__)
        logger.setLevel(self.level)
        formatter = logging.Formatter(self.message_format)
        formatter.datefmt = self.date_format
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.logger = logger
        self.app.log = self.log  # info level
        self.app.debug = partial(self.log, level=logging.DEBUG)

    def log(self, msg, level=logging.INFO):
        tb = traceback.extract_stack(limit=2)
        mod_name = os.path.basename(tb[0][0])
        lineno = tb[0][1]
        cur_level = level or self.level
        self.logger.log(cur_level, msg, extra={'mod_name': mod_name,
                                               'mod_line': lineno})

    def apply(self, callback, route):
        return callback
