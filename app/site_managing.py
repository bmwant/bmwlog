# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'

import os
from urlparse import urlparse
from bottle import request

from user_controller import require
from models import Photo, Banner
from helpers import post_get, redirect
from app import app, env, Config


@app.route('/banners')
@require('admin')
def banners_man():
    template = env.get_template('banners.html')

    if request.method == 'GET':
        return template.render()
    elif request.method == 'POST':
        pass


@app.route('/gallery_add', method=['GET', 'POST'])
@require('admin')
def gallery_add():
    template = env.get_template('gallery_add.html')
    if request.method == 'GET':
        return template.render()
    elif request.method == 'POST':
        photo_file = request.files.get('photo')
        gallery_folder = os.path.join(Config.ROOT_FOLDER, 'img/gallery/')
        file_path = os.path.join(gallery_folder, photo_file.filename)
        # photo_file.save('/img/gallery/')  # new Bottle
        with open(file_path, 'wb') as open_file:
            open_file.write(photo_file.file.read())

        photo = Photo.create(desc=post_get('desc'),
                             photo=photo_file.filename)
        app.flash(u'Фото успішно додане')
        redirect('/gallery_add')


@app.route('/banners', method=['GET', 'POST'])
@require('admin')
def gallery_add():
    template = env.get_template('banners.html')
    if request.method == 'GET':
        return template.render()
    elif request.method == 'POST':
        banner_img = request.files.get('banner_img')
        banners_folder = os.path.join(Config.ROOT_FOLDER, 'img/banners/')
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
        return template.render()

