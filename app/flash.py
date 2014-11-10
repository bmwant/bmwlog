from functools import wraps
from bottle import request, response, hook


class FlashPlugin(object):
    """
    Plugin for message flashing that supports categories
    """
    name = 'flash'
    api = 2

    def __init__(self, key='flash', secret=None):
        self.key = key
        self.secret = secret
        self.app = None

    def setup(self, app):
        self.app = app
        self.app.flash = self.flash
        self.app.get_flashed_messages = self.get_flashed_messages

    def load_flashed(self):
        m = request.get_cookie(key=self.key, secret=self.secret)
        if m is not None:
            response.flash_messages = m
            response.delete_cookie(self.key)

    def set_flashed(self):
        if hasattr(response, 'flash_messages'):
            response.set_cookie(name=self.key, 
                value=response.flash_messages, secret=self.secret)
            delattr(response, 'flash_messages')

    def flash(self, message, category='info'):
        """
        Categories: error, success, info
        """
        if not hasattr(response, 'flash_messages'):
            response.flash_messages = []
        response.flash_messages.append((message, category))

    def get_flashed_messages(self):
        if hasattr(response, 'flash_messages'):
            m = response.flash_messages
            delattr(response, 'flash_messages')
            response.delete_cookie(self.key)
            return m
            
    def apply(self, callback, route):
        def wrapper(*args, **kwargs):
            #self.load_flashed()
            rv = callback(*args, **kwargs)
            #self.set_flashed()
            return rv
        return wrapper
