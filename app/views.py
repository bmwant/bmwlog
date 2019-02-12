# -*- coding: utf-8 -*-
import os
import time

from bottle import request, abort
from peewee import fn

import app.controllers  # just to import all the available views
from app import models
from app import env
from app.controllers import require
from app.helpers import render_template, view, redirect, only_ajax
try:
    from gen_views import *
except ImportError:
    pass

from app import app, config

if config.DEBUG:
    from . import debug_views  # noqa


@app.route('/')
def index():
    redirect('/post')


@app.get('/joke')
@only_ajax
def get_joke():
    joke = models.SiteJoke.select().order_by(fn.Rand()).first()
    joke_text = 'ᕦ(ò_ó*)ᕤ     unexpected result'
    if joke is not None:
        joke_text = joke.text
    return {'text': joke_text}


@app.route('/categories')
@view('categories.html')
def categories():
    # todo: think and apply some join to get posts count
    cat_list = models.Category.select()

    def get_count(categ):
        return categ.posts_count
    categ_sorted = sorted(cat_list, key=get_count, reverse=True)

    return {'categories': categ_sorted}


@app.route('/about')
@view('about.html')
def about():
    pass


@app.route('/ad')
@require('admin')
def administration():
    return render_template('administration.html', link_what='admlink')


@app.route('/gallery')
@view('gallery.html')
def gallery():
    images = models.Photo.select()
    return {'images': images}


@app.get('/play')
@view('playground.html')
def playground():
    pass


@app.error(404)
def error404(error):
    template = env.get_template('errors/404.html')
    return template.render()


@app.error(500)
def error500(error):
    template = env.get_template('errors/500.html')
    return template.render()


@app.route('/sp/<page_name:re:[a-z\d_]+>')
def server_static(page_name):
    page = models.StaticPage.get_or_404(models.StaticPage.url == page_name)
    template = env.get_template('static_page.html')
    return template.render(page=page)


@app.get('/healthcheck')
def healthcheck():
    import psutil
    import humanfriendly

    now = time.time()
    pid = os.getgid()
    ppid = os.getppid()

    # how about launching under gunicorn?
    current_process = psutil.Process(pid=ppid)
    process_uptime = current_process.create_time()
    process_uptime_delta = now - process_uptime
    process_uptime_human = humanfriendly.format_timespan(process_uptime_delta)

    system_uptime = psutil.boot_time()
    system_uptime_delta = now - system_uptime
    system_uptime_human = humanfriendly.format_timespan(system_uptime_delta)

    free_memory = psutil.disk_usage('/').free
    free_memory_human = humanfriendly.format_size(free_memory)

    return {
        'status': 'Operational',
        'free_disk_space': free_memory_human,
        'system_uptime': system_uptime_human,
        'process_uptime': process_uptime_human,
    }
