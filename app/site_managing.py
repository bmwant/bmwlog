# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'

import os
from urlparse import urlparse
from bottle import request, abort

from models import Photo, Banner, Quote, DoesNotExist
from helpers import post_get, redirect, view
from helput import unique_filename
from user_controller import require
from forms import SimpleUploadForm
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
        gallery_folder = os.path.join(config.ROOT_FOLDER, 'img/gallery/')
        file_path = os.path.join(gallery_folder, photo_file.filename)
        # photo_file.save('/img/gallery/')  # new Bottle
        with open(file_path, 'wb') as open_file:
            open_file.write(photo_file.file.read())

        photo = Photo.create(desc=post_get('desc'),
                             photo=photo_file.filename)
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


@app.route('/quote_add', method=['GET', 'POST'])
@require('admin')
def quote_add():
    template = env.get_template('quote_add.html')
    if request.method == 'GET':
        quotes = Quote.select()
        return template.render({'quotes': quotes})
    elif request.method == 'POST':
        return template.render()


@app.get('/quote/delete/<id:int>')
@require('admin')
def quote_delete(id):
    try:
        quote = Quote.get(Quote.quote_id == id)
        quote.delete_instance()
        redirect('/quote_add')
    except DoesNotExist:
        abort(404)


@app.route('/upload', method=['GET', 'POST'])
@require('admin')
def upload():
    form = SimpleUploadForm()
    template = env.get_template('upload.html')
    if request.method == 'GET':
        return template.render(form=form)
    elif request.method == 'POST':
        up_file = request.files.get('file')
        folder = os.path.join(config.ROOT_FOLDER, 'img/article/')
        file_path = os.path.join(folder, up_file.filename)
        # photo_file.save('/img/gallery/')  # new Bottle
        with open(file_path, 'wb') as open_file:
            open_file.write(up_file.file.read())

        app.flash(u'Файл завантажено')
        redirect('/upload')


@app.route('/up', method=['POST'])
def up_file():
    up_file = request.files.get('file')
    folder = os.path.join(config.ROOT_FOLDER, 'img/article/')
    new_filename = unique_filename(up_file.filename)
    file_path = os.path.join(folder, new_filename)
    # photo_file.save('/img/gallery/')  # new Bottle
    with open(file_path, 'wb') as open_file:
        open_file.write(up_file.file.read())
    return 'Ok'