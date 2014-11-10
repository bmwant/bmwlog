# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'

import os
from wtforms import Form, FileField, SelectField, StringField, PasswordField,\
    validators
from helput import get_all_dirs, join_all_path
from helpers import save_file
from app import config


def get_up_folders():
    pass


class SimpleUploadForm(Form):
    file_folder = SelectField(u'Куди завантажити',
                              choices=[('img/article', u'Зображення до статті'), ('uploaded', u'Інші файли')],
                              validators=[validators.InputRequired()])
    upload_file = FileField(u'Виберіть файл',
                            validators=[validators.InputRequired()])
    """StringField('Email Address', [validators.Length(min=6, max=35)])
    accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])"""


class UploadFileField(FileField):
    def __init__(self, label='', validators=None, **kwargs):
        super(UploadFileField, self).__init__(label, validators, **kwargs)

    def process_formdata(self, valuelist):
        super(UploadFileField, self).process_formdata(valuelist)
        if self.data:
            f = save_file(self.data, 'img/users')
            self.data = f

    def __call__(self, *args, **kwargs):
        """
        Renders field with small pictogram
        """
        file_input = super(UploadFileField, self).__call__(*args, **kwargs)
        return file_input


class UserEditForm(Form):
    first_name = StringField(u'Ім\'я')
    last_name = StringField(u'Прізвище')
    nickname = StringField(u'Псевдонім')
    picture = UploadFileField(u'Фото')

    def populate_obj(self, obj):
        if not self.picture.data:
            delattr(self, 'picture')
        super(UserEditForm, self).populate_obj(obj)


class SignupForm(Form):
    mail = StringField(u'E-mail', validators=[validators.Email()])
    password = PasswordField(u'Пароль', validators=[validators.InputRequired(), validators.Length(min=6)])
    first_name = StringField(u'Ім\'я', validators=[validators.InputRequired()])
    last_name = StringField(u'Прізвище', validators=[validators.InputRequired()])
    nickname = StringField(u'Нік', validators=[validators.InputRequired()])

