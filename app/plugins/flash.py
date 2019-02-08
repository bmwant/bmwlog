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

    def flash(self, message, category='info'):
        """
        Categories: error, success, info
        """
        if not hasattr(response, 'flash_messages'):
            response.flash_messages = []
        response.flash_messages.append((message, category))

    def get_flashed_messages(self):
        if hasattr(response, 'flash_messages'):
            messages = response.flash_messages
            delattr(response, 'flash_messages')
            return messages
            
    def apply(self, callback, route):
        def wrapper(*args, **kwargs):
            rv = callback(*args, **kwargs)
            return rv
        return wrapper
