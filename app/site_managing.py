# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'

import os
from urlparse import urlparse
from bottle import request, abort, static_file
from geventwebsocket import WebSocketError

from models import Photo, Banner, Quote, DoesNotExist, StaticPage, StreamMessage
from helpers import post_get, redirect, view, backup_db, only_ajax
from helput import unique_filename, join_all_path, generate_filename, distort_filename
from user_controller import require
from forms import SimpleUploadForm, StaticPageForm
from app import app, env, config


@app.route('/gallery_add', method=['GET', 'POST'])
@require('admin')
def gallery():
    template = env.get_template('gallery_add.html')
    if request.method == 'GET':
        photos = Photo.select()
        return template.render(photos=photos)
    elif request.method == 'POST':
        photo_file = request.files.get('photo')

        file_ext = os.path.splitext(photo_file.filename)[1]
        print(file_ext)
        gallery_folder = os.path.join(config.ROOT_FOLDER, 'img/gallery/')
        f_name = generate_filename(prefix='photo') + file_ext
        file_path = os.path.join(gallery_folder, f_name)
        # photo_file.save('/img/gallery/')  # new Bottle
        with open(file_path, 'wb') as open_file:
            open_file.write(photo_file.file.read())

        photo = Photo.create(desc=post_get('desc'),
                             photo=f_name)
        app.flash(u'Фото успішно додане')
        redirect('/gallery_add')


@app.get('/photo/delete/<id:int>')
@require('admin')
def photo_delete(id):
    try:
        photo = Photo.get(Photo.photo_id == id)
        photo.delete_instance()
        redirect('/gallery_add')
    except DoesNotExist:
        abort(404)


@app.route('/banners', method=['GET', 'POST'])
@require('admin')
def banners():
    template = env.get_template('banners.html')
    if request.method == 'GET':
        all_banners = Banner.select()
        return template.render({'banners': all_banners})
    elif request.method == 'POST':
        banner_img = request.files.get('banner_img')
        banners_folder = os.path.join(config.ROOT_FOLDER, 'img/banners/')
        file_path = os.path.join(banners_folder, banner_img.filename)
        # photo_file.save('/img/gallery/')  # new Bottle
        with open(file_path, 'wb') as open_file:
            open_file.write(banner_img.file.read())

        link = post_get('link')
        up = urlparse(link)
        if up.scheme == '':
            link = 'http://{0}'.format(link)

        banner = Banner.create(desc=post_get('desc'),
                               link=link,
                               img=banner_img.filename)
        app.flash(u'+1 новий банер')
        redirect('/banners')


@app.get('/banner/delete/<id:int>')
@require('admin')
def banner_delete(id):
    try:
        banner = Banner.get(Banner.banner_id == id)
        banner.delete_instance()
        redirect('/banners')
    except DoesNotExist:
        abort(404)


@app.route('/quote/add', method=['GET', 'POST'])
@require('admin')
def quote_add():
    template = env.get_template('quote_add.html')
    all_quotes = Quote.select()
    if request.method == 'POST':
        quote = Quote.create(text=post_get('text'),
                             author=post_get('author'))
        app.flash(u'Цитата додана', 'success')
    return template.render({'quotes': all_quotes})


@app.get('/quote/delete/<quote_id:int>')
@require('admin')
def quote_delete(quote_id):
    try:
        quote = Quote.get(Quote.quote_id == quote_id)
        quote.delete_instance()
        app.flash(u'Цитата видалена', 'success')
        redirect('/quote/add')
    except DoesNotExist:
        abort(404)


@app.route('/upload', method=['GET', 'POST'])
@require('admin')
def upload():
    """
    Uploads a file to the site storage on the server
    """
    #todo: add auto-rename
    #todo: add format checking and size for pictures
    form = SimpleUploadForm(request.POST)
    template = env.get_template('upload.html')
    if request.method == 'POST' and form.validate():
        up_file = form.upload_file.data
        folder = os.path.join(config.ROOT_FOLDER, form.file_folder.data)
        if not os.path.exists(folder):
            os.makedirs(folder)
        new_filename = up_file.filename
        file_path = os.path.join(folder, new_filename)
        #Generate unique filename if one already exists
        if os.path.exists(file_path):
            new_filename = distort_filename(up_file.filename)
            file_path = os.path.join(folder, new_filename)
        # photo_file.save('/img/gallery/')  # new Bottle
        with open(file_path, 'wb') as open_file:
            open_file.write(up_file.file.read())
        uploaded_file = join_all_path(['/', form.file_folder.data, new_filename]).replace('\\', '/')
        app.flash(u'Файл завантажено')
        return template.render(form=form, uploaded_file=uploaded_file)
    return template.render(form=form)


@app.route('/up', method=['POST'])
def up_file():
    """
    Uploads a picture to the article
    """
    up_file = request.files.get('file')
    web_folder = 'img/article/'
    folder = os.path.join(config.ROOT_FOLDER, web_folder)
    new_filename = unique_filename(up_file.filename)
    file_path = os.path.join(folder, new_filename)
    #todo: check for file existence
    # photo_file.save('/img/gallery/')  # new Bottle
    with open(file_path, 'wb') as open_file:
        open_file.write(up_file.file.read())
    return join_all_path(['/', web_folder, new_filename])


@app.get('/ad/backupdb')
def backdb():
    backup_name = backup_db()
    backup_file = join_all_path([config.ROOT_FOLDER, 'uploaded', backup_name])
    root_f = join_all_path([config.ROOT_FOLDER, 'uploaded'])
    return static_file(backup_name, root=root_f, download=backup_name)


@app.route('/sp/add', method=['GET', 'POST'])
@require('admin')
def sp_add():
    form = StaticPageForm(request.POST)
    template = env.get_template('static_page_admin.html')

    if form.validate_on_post():
        app.log(form.page_url.data)
        new_page = StaticPage.create(title=form.title.data,
                                     url=form.page_url.data,
                                     text=form.text.data)
        app.flash('New page!')
    pages = StaticPage.select()
    return template.render(form=form, pages=pages)


@app.get('/sp/delete/<sp_id:int>')
@require('admin')
def sp_delete(sp_id):
    try:
        sp = StaticPage.get(StaticPage.id == sp_id)
        sp.delete_instance()
        app.flash(u'Сторінка видалена', 'success')
        redirect('/sp/add')
    except DoesNotExist:
        abort(404)


@app.post('/sm/add')
def sm_add():
    """
    Add new stream message
    """
    message = post_get('message')
    new_message = StreamMessage(message=message)
    new_message.save()
    return 'Ok'


@app.get('/banner/disable/<banner_id:int>')
@only_ajax
@require('admin')
def disable_banner(banner_id):
    banner = Banner.get_or_404(Banner.banner_id == banner_id)
    banner.disabled = not banner.disabled
    banner.save()
    return 'Ok'


@app.route('/websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    while True:
        try:
            message = wsock.receive()
            wsock.send("Your message was: %r" % message)
        except WebSocketError:
            break
