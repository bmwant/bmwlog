# -*- coding: utf-8 -*-

from bottle import static_file, error, request, post
from models import *
from post_controller import *
from user_controller import *
from helpers import view, redirect
from app import app

from helput import get_list_of_files


@app.route('/')
def index():
    if app.current_user is not None:
        print(app.current_user.role.role)
    redirect('/post')


@app.route('/categories')
@view('categories.html')
def categories():
    cat_list = Category.select()
    return {'link_what': 'catlink', 'items': cat_list}


@app.route('/about')
@view('about.html')
def about():
    return {'link_what': 'abtlink'}


@app.route('/administration')
@require('admin')
def administration():
    template = env.get_template('administration.html')
    return template.render(link_what='admlink')


@app.route('/gallery')
@view('gallery.html')
def administration():
    images = get_list_of_files(r'D:\coding\bmwlog\img\gallery', ext='.jpg', full_path=False)
    return {'link_what': 'gallink', 'images': images}


@app.error(404)
def error404(error):
    template = env.get_template('404.html')
    return template.render()


#serving static files
@app.route('/<folder>/<filename:path>')
def server_static(folder, filename):
    from app import Config
    return static_file(filename, root=Config.STATIC_FOLDER+folder)
