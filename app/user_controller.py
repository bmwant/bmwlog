# -*- coding: utf-8 -*-
from bottle import route, request, response, abort
from jinja2 import Environment, PackageLoader
from models import User, DoesNotExist, Role
from app import app, env
from helpers import post_get, redirect
from functools import wraps


def require(role):
    """
    Allows user that have at least the role to access the resource
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if app.current_user is not None:
                r = Role.get(Role.role == role)
                if app.current_user.role.level >= r.level:
                    return func(*args, **kwargs)
                app.flash(u'У Вас недостатньо прав для перегляду')
                redirect()
            app.flash(u'Увійдіть, щоб переглянути дану сторінку')
            redirect('/login')
        return wrapper
    return decorator


def authorize(func):
    '''
    User needs to be logged in
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        if app.current_user is not None:
            return func(*args, **kwargs)
        app.flash(u'Увійдіть, щоб переглянути дану сторінку')
        redirect('/login')
    return wrapper


@app.route('/login', method=['GET', 'POST'])
def login():
    if app.current_user is not None:
        print('Ok we are here')
        app.flash(u'Вийдіть з поточної сесії, щоб увійти під іншим акаунтом')
        redirect()
    if request.method == 'POST':
        try:
            user = User.get(User.mail == post_get('email'))
        except DoesNotExist:
            app.flash('There is no user with such email')
        else:
            if user.user_password == User.encode_password(
                    post_get('password')):
                app.flash(u'Ви успішно увійшли')
                app.login(user)
                redirect()
            else:
                app.flash(u'Невірний пароль')

    template = env.get_template('user/login.html')

    return template.render()


@app.route('/signup', method=['GET', 'POST'])
def signup():
    template = env.get_template('user/signup.html')
    if request.method == 'GET':
        return template.render()
    if request.method == 'POST':
        try:
            user = User.get(User.mail == post_get('email'))
        except DoesNotExist:
            new_user = User.create(first_name=request.forms.get('fname'),
                                   last_name=request.forms.get('lname'),
                                   nickname=request.forms.get('nickname'),
                                   user_password=User.encode_password(
                                       request.forms.get('password')),
                                   mail=request.forms.get('email'))
            app.flash(u'Реєстрація пройшла успішно')
            return redirect('/')
        else:
            app.flash(u'Користувач з такою поштою уже існує')
            return template.render()


@app.get('/logout')
@authorize
def logout():
    app.logout()
    app.flash(u'Ви успішно вийшли')
    redirect()
