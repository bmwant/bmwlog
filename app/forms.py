# -*- coding: utf-8 -*-
import wtforms
from bottle import request
from wtforms import (FileField, SelectField, StringField, PasswordField,
                     validators, TextAreaField)

from app.models import User
from helput import translit_text
from helpers import save_file


class Form(wtforms.Form):
    def validate_on_post(self):
        if request.method in ('POST', 'PUT'):
            return super(Form, self).validate()
        return False

    def populate_obj(self, obj):
        for name, field in self._fields.items():
            if hasattr(field, 'target_name'):
                field.populate_obj(obj, field.target_name)
            else:
                field.populate_obj(obj, name)


class SimpleUploadForm(Form):
    upload_choices = (
        ('img/article', u'Зображення до статті'),
        ('uploaded', u'Інші файли'),
    )
    file_folder = SelectField(u'Куди завантажити',
                              choices=upload_choices,
                              validators=[validators.InputRequired()])
    upload_file = FileField(u'Виберіть файл',
                            validators=[validators.InputRequired()])


class UploadFileField(FileField):
    def __init__(self, label=u'', validators=None, **kwargs):
        super(UploadFileField, self).__init__(label, validators, **kwargs)

    def process_formdata(self, valuelist):
        super(UploadFileField, self).process_formdata(valuelist)
        if self.data:
            f = save_file(self.data, 'img/users')
            self.data = f

    def __call__(self, **kwargs):
        """
        Renders field with small pictogram
        """
        file_input = super(UploadFileField, self).__call__(**kwargs)
        return file_input


class ConfirmPasswordField(PasswordField):
    def __init__(self, *args, **kwargs):
        if 'target_name' in kwargs:
            self.target_name = kwargs.pop('target_name')

        super(ConfirmPasswordField, self).__init__(*args, **kwargs)

    def __call__(self, **kwargs):
        return super(ConfirmPasswordField, self).__call__(**kwargs)

    def process_formdata(self, valuelist):
        if valuelist and isinstance(valuelist[0], str):
            value = User.encode_password(valuelist[0])
            valuelist = (value, )
        return super(ConfirmPasswordField, self).process_formdata(valuelist)



class UserEditForm(Form):
    first_name = StringField(u'Ім\'я')
    last_name = StringField(u'Прізвище')
    nickname = StringField(u'Псевдонім')
    picture = UploadFileField(u'Фото')
    change_password = ConfirmPasswordField(target_name='user_password')

    def populate_obj(self, obj):
        if not self.picture.data:
            delattr(self, 'picture')

        if not self.change_password.data:
            del self['change_password']

        super(UserEditForm, self).populate_obj(obj)


class SignupForm(Form):
    mail = StringField(u'E-mail', validators=[validators.Email()])
    password = PasswordField(u'Пароль',
                             validators=[validators.InputRequired(),
                                         validators.Length(min=6)])
    first_name = StringField(u'Ім\'я', validators=[validators.InputRequired()])
    last_name = StringField(u'Прізвище',
                            validators=[validators.InputRequired()])
    nickname = StringField(u'Нік', validators=[validators.InputRequired()])


class StaticPageForm(Form):
    title = StringField(
        u'Назва сторінки',
        validators=[validators.InputRequired()],
    )
    page_url = StringField('Url')
    text = TextAreaField(
        u'Текст сторінки',
        validators=[validators.InputRequired()],
    )

    def validate_page_url(self, field):
        if not field.data:
            field.data = translit_text(self.title.data)
