# -*- coding: utf-8 -*-
from bottle import request, response
from app.models import User, DoesNotExist, Session


class LoginManager(object):
    name = 'lm'  # Login manager
    api = 2

    def __init__(self, key='ses_mngr', secret=None):
        self.key = key
        self.secret = secret
        self.app = None
        self.session_id = None

    def setup(self, app):
        self.app = app
        self.app.current_user = None
        self.app.login = self.login
        self.app.logout = self.logout

    def load_user(self):
        if self.session_id is not None:
            self.app.log(self.session_id)
            session = Session.get(Session.session_id == self.session_id)
            if session.active:
                self.app.current_user = User.get(User.mail == session.mail)
            else:
                self.app.current_user = None
                self.session_id = None
        else:
            self.app.current_user = None

    def login(self, user):
        session = Session(mail=user.mail,
                          expires=5 * 24 * 60 * 60)
        session.save()
        self.session_id = session.session_id
        self.app.current_user = user
        self.set_session()

    def logout(self):
        self.app.log('Logout user: %s.' % self.app.current_user)
        self.app.current_user = None
        session = Session.get(Session.session_id == self.session_id)
        session.active = False
        session.save()
        self.session_id = None
        response.delete_cookie(self.key)

    def set_session(self):
        if self.app.current_user is not None:
            self.app.log('Setting session value for: %s.' % self.app.current_user)
            response.set_cookie(name=self.key,
                                value=self.session_id,
                                secret=self.secret,
                                path='/',
                                httponly=True)
        else:
            response.delete_cookie(self.key)

    def apply(self, callback, route):
        def wrapper(*args, **kwargs):
            self.app.log('My session id: %s' % self.session_id)
            self.load_user()
            rv = callback(*args, **kwargs)
            self.set_session()
            return rv
        return wrapper
