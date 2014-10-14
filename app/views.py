# -*- coding: utf-8 -*-

from bottle import static_file, error, request, post
from helpers import view, redirect
from helput import get_list_of_files

from models import *

from post_controller import *
from user_controller import *
from site_managing import *

from app import app, config


@app.route('/')
def index():
    app.log(request.get_cookie('login_manager', secret='some-secret-key'), 'info')
    print('what is it')
    redirect('/post')


@app.route('/categories')
@view('categories.html')
def categories():
    #todo: think and apply some join to get posts count
    cat_list = Category.select()
    categ = {}
    for category in cat_list:
        categ[category.category_id] = {
            'name': category.category_name,
            'posts_count': Post.select().where(Post.category == category).count()
        }
    return {'link_what': 'catlink', 'categories': categ}


@app.route('/about')
@view('about.html')
def about():
    return {'link_what': 'abtlink'}


@app.route('/ad')
@require('admin')
def administration():
    template = env.get_template('administration.html')
    return template.render(link_what='admlink')


@app.route('/gallery')
@view('gallery.html')
def gallery():
    #images = get_list_of_files(r'D:\coding\bmwlog\img\gallery', ext='.jpg', full_path=False)
    images = Photo.select()
    return {'link_what': 'gallink', 'images': images}



@app.error(404)
def error404(error):
    template = env.get_template('404.html')
    return template.render()


#serving static files
@app.route('/<folder>/<filename:path>')
def server_static(folder, filename):
    return static_file(filename, root=config.STATIC_FOLDER+folder)

@app.route('/favicon.ico')
def serve_favicon():
    return static_file('favicon.ico', root=config.STATIC_FOLDER)
