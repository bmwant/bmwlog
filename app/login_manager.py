from bottle import request, response
from .models import User, DoesNotExist


class LoginManager(object):
    name = 'login_manager'
    api = 2

    def __init__(self, key='login_manager', secret=None):
        self.key = key
        self.secret = secret
        self.app = None

    def setup(self, app):
        self.app = app
        #self.app.add_hook('before_request', self.load_user)
        #self.app.add_hook('after_request', self.set_user)
        self.app.current_user = None
        self.app.login = self.login
        self.app.logout = self.logout

    def load_user(self):
        #todo: add check if invalid cookie is provided
        usermail = request.get_cookie(self.key, secret=self.secret)
        self.app.log('Try to login this user: %s' % usermail)
        if len(request.cookies.getall(self.key)) > 1:
            return self.logout()

        if usermail is not None:
            try:
                self.app.current_user = User.get(User.mail == usermail)
            except DoesNotExist:
                self.logout()
        self.app.log('User loaded: %s' % self.app.current_user)

    def login(self, user):
        self.app.current_user = user
        self.set_user()

    def logout(self):
        self.app.log('Logout user: %s.' % self.app.current_user)
        self.app.current_user = None
        self.app.log('Now offline?: %s.' % self.app.current_user)
        response.delete_cookie(self.key, path='/')


    def set_user(self):
        self.app.log('Setting user after request: %s.' % self.app.current_user)
        if self.app.current_user is not None:
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
            cookie_del = request.get_cookie(self.key, secret=self.secret)
            self.app.log('Delete cookie: %s' % cookie_del)
            return rv
        return wrapper
