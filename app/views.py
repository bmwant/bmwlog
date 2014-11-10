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
    redirect('/post')


@app.get('/try')
def tr():
    from .helput import translit_url
    print(translit_url())
    app.log('Message')
    template = env.get_template('info.html')
    quote = Quote.select().first()
    messages = StreamMessage.select()
    return template.render(messages=messages, quote=quote)


@app.route('/categories')
@view('categories.html')
def categories():
    #todo: think and apply some join to get posts count
    cat_list = Category.select()
    categ = {}
    for category in cat_list:
        categ[category.category_id] = {
            'name': category.category_name,
            'posts_count': Post.get_posts().where(Post.category == category).count()
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


@app.get('/playground')
def playground():
    return 'NotImplementedError :)'


@app.route('/tr')
def try_route():
    template = env.get_template('info.html')
    return template.render(value='one hundred')


@app.error(404)
def error404(error):
    template = env.get_template('404.html')
    return template.render()


@app.route('/sp/<page_name:re:[a-z\d_]+>')
def server_static(page_name):
    try:
        page = StaticPage.get(StaticPage.url == page_name)
    except DoesNotExist:
        abort(404)
    template = env.get_template('static_page.html')
    return template.render(page=page)

#serving static files
@app.route('/<folder>/<filename:path>')
def server_static(folder, filename):
    return static_file(filename, root=config.STATIC_FOLDER+folder)

@app.route('/favicon.ico')
def serve_favicon():
    return static_file('favicon.ico', root=config.STATIC_FOLDER)
