# -*- coding: utf-8 -*-
#load configuration first
import sys
sys.path.insert(0, 'py')
from config import *
from bottle import route, run, static_file, redirect, error, request, get, \
    post, default_app, view, jinja2_view
from models import *
from cork.backends import SqlAlchemyBackend

from jinja2 import Environment, PackageLoader
from cork import Cork
from beaker.middleware import SessionMiddleware


env = Environment(loader=PackageLoader('bmwlog', 'templates'))

aaa = Cork('auth')

authorize = aaa.make_auth_decorator(fail_redirect='/login', role='admin')
from post_controller import *
from user_controller import *


@route('/')
def index():
    redirect('/post')


@route('/categories')
def categories():
    cat_list = Category.select()
    template = env.get_template('categories.html')
    return template.render(link_what="catlink", items=cat_list)

@route('/about')
def about():
    aaa.require(fail_redirect='/login')
    template = env.get_template('about.html')
    return template.render(link_what='abtlink')


@route('/admin')
@authorize(role="admin", fail_redirect='/sorry_page')
def admin():
    """Only admin users can see this"""
    #aaa.require(role='admin', fail_redirect='/sorry_page')
    #return dict(
    #    current_user=aaa.current_user,
    #    users=aaa.list_users(),
    #    roles=aaa.list_roles()
    #)
    template = env.get_template('admin_page.html')
    return template.render(current_user=aaa.current_user,
                           users=aaa.list_users(),
                           roles=aaa.list_roles())



@route('/administration')
@authorize(role="admin")
def administration():
    template = env.get_template('administration.html')
    return template.render(link_what='admlink')

@error(404)
def error404(error):
    template = env.get_template('404.html')
    return template.render()

#serving static files
@route('/<folder>/<filename>')
def server_static(folder, filename):
    return static_file(filename, root='D:/coding/bmwlog/'+folder)


@route('/login', method='POST')
def login():
    mail = request.POST.get('email', '')
    user_password = request.POST.get('password', '')
    aaa.login(mail, user_password, success_redirect='/', fail_redirect='/login')

@route('/logout')
def logout():
    aaa.logout(success_redirect='/login')

# @bottle.route('/')
# def index():
#     """Only authenticated users can see this"""
#     aaa.require(fail_redirect='/sorry_page')
#     return "Welcome %s" % aaa.current_user.username


@route('/register', method='POST')
def register():
    """Users can create new accounts, but only with 'user' role"""
    username = request.POST.get('user', '')
    password = request.POST.get('pwd', '')
    email_addr = request.POST.get('email_addr', '')
    aaa.register(username, password, email_addr)
    return 'Please check your inbox.'


# Web application main

def main():
    session_opts = {
        'session.type': 'cookie',
        'session.validate_key': True,
        'session.cookie_expires': True,
        'session.timeout': 3600 * 24 * 5,  # 5 days
        'session.encrypt_key': 'random-key-combo',
    }
    app = default_app()
    app = SessionMiddleware(app, session_opts)

    run(app=app, host='localhost', port=8081, debug=True, reloader=True)

if __name__ == "__main__":
    main()
