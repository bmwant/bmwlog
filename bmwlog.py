# -*- coding: utf-8 -*-
#load configuration first
from config import *
from bottle import route, run, static_file, redirect, error, request, get, post, default_app
from models import *

from jinja2 import Environment, PackageLoader
from cork import Cork
from beaker.middleware import SessionMiddleware

aaa = Cork('proto')
env = Environment(loader=PackageLoader('bmwlog', 'templates'))

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
def categories():
    template = env.get_template('about.html')
    return template.render(link_what='abtlink')

@route('/administration')
def categories():
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
    username = request.POST.get('user', '')
    password = request.POST.get('pwd', '')
    aaa.login(username, password, success_redirect='/', fail_redirect='/login')

@route('/logout')
def logout():
    aaa.current_user.logout(redirect='/login')

# @bottle.route('/')
# def index():
#     """Only authenticated users can see this"""
#     aaa.require(fail_redirect='/sorry_page')
#     return "Welcome %s" % aaa.current_user.username

@route('/admin')
def admin():
    """Only administrators can see this"""
    aaa.require(role='admin', fail_redirect='/sorry_page')
    return 'Welcome administrators'

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
    }
    app = default_app()
    app = SessionMiddleware(app, session_opts)

    run(app=app, host='localhost', port=8081, debug=True)

if __name__ == "__main__":
    main()
