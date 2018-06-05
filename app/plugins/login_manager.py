import logging

from bottle import request, response
from app.models import User, DoesNotExist


class LoginManager(object):
    name = 'login_manager'
    api = 2

    def __init__(self, key='login_manager', secret=None,
                 enable_journaling=False):
        self.key = key
        self.secret = secret
        self.app = None
        self.enable_journaling = enable_journaling

    def setup(self, app):
        self.app = app
        # self.app.add_hook('before_request', self.load_user)
        # self.app.add_hook('after_request', self.set_user)
        self.app.current_user = None
        self.app.login = self.login
        self.app.logout = self.logout

    def _log(self, msg):
        """
        Use app logger if corresponding plugin has been installed and regular
        print otherwise
        """
        if not self.enable_journaling:
            return

        if hasattr(self.app, 'log'):
            self.app.log(msg, level=logging.DEBUG)
        else:
            print(msg)

    def load_user(self):
        try:
            usermail = request.get_cookie(self.key, secret=self.secret)
        except ValueError:
            self._log('Invalid cookie, forcing logout')
            return self.logout()

        if len(request.cookies.getall(self.key)) > 1:
            return self.logout()

        if usermail is not None:
            try:
                self._log('Try to login this user: %s' % usermail)
                self.app.current_user = User.get(User.mail == usermail)
            except DoesNotExist:
                self.logout()
        else:
            self.app.current_user = None
        self._log('User loaded: %s' % self.app.current_user)

    def login(self, user):
        self.app.current_user = user
        self.set_user()

    def logout(self):
        self._log('Logout user: %s.' % self.app.current_user)
        self.app.current_user = None
        self._log('Now offline?: %s.' % self.app.current_user)
        response.delete_cookie(self.key, path='/')

    def set_user(self):
        if self.app.current_user is not None:
            self._log('Setting user after request: {current_user}'.format(
                current_user=self.app.current_user))

            response.set_cookie(name=self.key,
                                value=self.app.current_user.mail,
                                secret=self.secret,
                                path='/',
                                httponly=True,
                                max_age=5 * 24 * 60 * 60)  # 5 days in seconds

    def apply(self, callback, route):
        def wrapper(*args, **kwargs):
            self.load_user()
            rv = callback(*args, **kwargs)
            self.set_user()
            return rv
        return wrapper
