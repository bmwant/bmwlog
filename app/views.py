# -*- coding: utf-8 -*-
from bottle import static_file, redirect, error, request, \
    post, view, jinja2_view, Bottle, install
from bottle import jinja2_view as view, jinja2_template as template
from bottle_flash import FlashPlugin
from models import *
from post_controller import *
from user_controller import *

from app import app

def postd():
    return bottle.request.forms


def post_get(name, default=''):
    return bottle.request.POST.get(name, default).strip()


@app.route('/')
def index():
    redirect('/post')



@app.route('/categories')
def categories():
    cat_list = Category.select()
    template = env.get_template('categories.html')
    return template.render(link_what="catlink", items=cat_list)


@app.route('/about')
def about():
    template = env.get_template('about.html')
    return template.render(link_what='abtlink')


@app.route('/administration')
def administration():
    template = env.get_template('administration.html')
    return template.render(link_what='admlink')


@app.error(404)
def error404(error):
    template = env.get_template('404.html')
    return template.render()


#serving static files
@app.route('/<folder>/<filename>')
def server_static(folder, filename):
    return static_file(filename, root='R:/proge/bmwlog/'+folder)
