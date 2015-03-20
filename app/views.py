# -*- coding: utf-8 -*-

from bottle import static_file, error, request, post
from helpers import view, redirect, render_template
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
    app.flash('Trying flashing bying', 'error')
    tg = Tag.get(Tag.tag_id == 36)
    print(tg.posts_count)
    quote = Quote.select().first()
    messages = StreamMessage.select()
    return render_template('info.html', messages=messages, quote=quote)


@app.get('/joke')
@only_ajax
def get_joke():
    joke = SiteJoke.select().order_by(fn.Rand()).first()
    return json.dumps({'text': joke.text})


@app.route('/categories')
@view('categories.html')
def categories():
    #todo: think and apply some join to get posts count
    cat_list = Category.select()

    def get_count(categ):
        return categ.posts_count
    categ_sorted = sorted(cat_list, key=get_count, reverse=True)

    return {'link_what': 'catlink', 'categories': categ_sorted}


@app.route('/about')
@view('about.html')
def about():
    return {'link_what': 'abtlink'}


@app.route('/ad')
@require('admin')
def administration():
    return render_template('administration.html', link_what='admlink')


@app.route('/gallery')
@view('gallery.html')
def gallery():
    #images = get_list_of_files(r'D:\coding\bmwlog\img\gallery', ext='.jpg', full_path=False)
    images = Photo.select()
    return {'link_what': 'gallink', 'images': images}


@app.get('/playground')
@view('playground.html')
def playground():
    return {'link_what': 'playground'}


@app.error(404)
def error404(error):
    template = env.get_template('404.html')
    return template.render()


@app.route('/sp/<page_name:re:[a-z\d_]+>')
def server_static(page_name):
    page = StaticPage.get_or_404(StaticPage.url == page_name)
    template = env.get_template('static_page.html')
    return template.render(page=page)


if config.DEBUG:
    #serving static files
    @app.route('/<folder>/<filename:path>')
    def server_static(folder, filename):
        return static_file(filename, root=config.STATIC_FOLDER+folder)

    @app.route('/favicon.ico')
    def serve_favicon():
        return static_file('favicon.ico', root=config.STATIC_FOLDER)
