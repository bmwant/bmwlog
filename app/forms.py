# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'

import os
from wtforms import Form, FileField, SelectField, StringField, validators
from helput import get_all_dirs, join_all_path
from app import config


def get_up_folders():
    pass


class SimpleUploadForm(Form):
    file_folder = SelectField(u'Куди завантажити',
                              choices=[('/img/article', u'Зображення до статті'), ('/uploaded', u'Інші файли')],
                              validators=[validators.InputRequired()])
    upload_file = FileField(u'Виберіть файл',
                            validators=[validators.InputRequired()])
    """StringField('Email Address', [validators.Length(min=6, max=35)])
    accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])"""