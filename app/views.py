# -*- coding: utf-8 -*-
import os
import time

from bottle import static_file, error, request, post
from helpers import view, redirect, render_template
from helput import get_list_of_files

from models import *

from post_controller import *
from user_controller import *
from site_managing import *
try:
    from gen_views import *
except ImportError:
    pass


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
    joke_text = u'ᕦ(ò_ó*)ᕤ     неочікуваний результат'
    if joke is not None:
        joke_text = joke.text
    return {'text': joke_text}


@app.route('/categories')
@view('categories.html')
def categories():
    # todo: think and apply some join to get posts count
    cat_list = Category.select()

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
    #images = get_list_of_files(r'D:\coding\bmwlog\img\gallery', ext='.jpg', full_path=False)
    images = Photo.select()
    return {'images': images}


@app.get('/playground')
@view('playground.html')
def playground():
    pass


@app.error(404)
def error404(error):
    template = env.get_template('404.html')
    return template.render()


@app.route('/sp/<page_name:re:[a-z\d_]+>')
def server_static(page_name):
    page = StaticPage.get_or_404(StaticPage.url == page_name)
    template = env.get_template('static_page.html')
    return template.render(page=page)


@app.get('/healthcheck')
def healthcheck():
    import psutil
    import humanfriendly

    now = time.time()
    pid = os.getgid()
    ppid = os.getppid()

    current_process = psutil.Process(pid=ppid)  # how about launching under gunicorn?
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


if config.DEBUG:
    # serving static files
    root = os.path.expanduser(config.STATIC_FOLDER)

    @app.route('/<folder>/<filename:path>')
    def server_static(folder, filename):
        return static_file(filename, root=root+folder)

    @app.route('/favicon.ico')
    def serve_favicon():
        return static_file('favicon.ico', root=root)


@app.route('/websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected Weesoo request.')

    while True:
        try:
            message = wsock.receive()
            wsock.send('Your message %s' % message)
        except WebSocketError:
            break
