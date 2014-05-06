from functools import wraps
from bottle import request, response

class FlashPlugin(object):
    '''
    What's wrong with this stupid bottle?
    '''
    name = 'flash'
    api = 2

    def __init__(self, key='flash', secret=None):
        self.key = key
        self.secret = secret
        self.app = None

    def setup(self, app):
        self.app = app
        # self.app.hooks.add('before_request', self.load_flashed)
        # self.app.hooks.add('after_request', self.set_flashed)
        self.app.flash = self.flash
        self.app.get_flashed_messages = self.get_flashed_messages

    def load_flashed(self):
        pass
        # m = request.get_cookie(key=self.key, secret=self.secret)
        # print(m)
        # if m is not None:
        #     print('Iamhere')
        #     response.flash_messages = m

    def set_flashed(self):
        pass
        # if hasattr(response, 'flash_messages'):
        #     response.set_cookie(name=self.key, 
        #         value=response.flash_messages, secret=self.secret)
        #     delattr(response, 'flash_messages')

    def flash(self, message):
        if not hasattr(response, 'flash_messages'):
            response.flash_messages = []
        response.flash_messages.append(message)

    def get_flashed_messages(self):
        if hasattr(response, 'flash_messages'):
            m = response.flash_messages
            delattr(response, 'flash_messages')
            # response.delete_cookie(self.key)
            return m
            
    def apply(self, callback, context):
        return callback
