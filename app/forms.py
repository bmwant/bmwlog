# -*- coding: utf-8 -*-
import wtforms
from bottle import request
from wtforms import (
    FileField,
    SelectField,
    StringField,
    BooleanField,
    PasswordField,
    TextAreaField,
)
from wtforms import validators
from app.fields import (
    OnOffField,
    UploadFileField,
    LanguageSelectField,
    ConfirmPasswordField,
    AutoFocusTextInput,
)
from app.helput import translit_text


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


class ItemForm(Form):
    def __init__(self, *args, **kwargs):
        model_class = kwargs.pop('model_class')
        url_prefix = kwargs.pop('url_prefix', None)

        self._model = model_class
        self.url_prefix = url_prefix or model_class.__name__.lower()
        super(ItemForm, self).__init__(*args, **kwargs)

    @property
    def classname(self):
        return self._model.__name__


class SimpleUploadForm(Form):
    upload_choices = (
        ('img/article', u'Зображення до статті'),
        ('uploaded', u'Інші файли'),
    )
    file_folder = SelectField('Upload destination',
                              choices=upload_choices,
                              validators=[validators.InputRequired()])
    upload_file = FileField('Choose a file',
                            validators=[validators.InputRequired()])


class UserEditForm(Form):
    first_name = StringField('Name')
    last_name = StringField('Last name')
    nickname = StringField('Nickname')
    picture = UploadFileField('Profile picture')
    change_password = ConfirmPasswordField(target_name='user_password')

    def populate_obj(self, obj):
        if not self.picture.data:
            delattr(self, 'picture')

        if not self.change_password.data:
            del self['change_password']

        super(UserEditForm, self).populate_obj(obj)


class SignupForm(Form):
    mail = StringField('E-mail', validators=[validators.Email()])
    password = PasswordField('Password',
                             validators=[validators.InputRequired(),
                                         validators.Length(min=6)])
    first_name = StringField('Name', validators=[validators.InputRequired()])
    last_name = StringField('Last name',
                            validators=[validators.InputRequired()])
    nickname = StringField('Nickname', validators=[validators.InputRequired()])


class StaticPageForm(ItemForm):
    title = StringField(
        'Page name',
        validators=[validators.InputRequired()],
    )
    page_url = StringField('URL')
    text = TextAreaField(
        'Content',
        validators=[validators.InputRequired()],
    )

    def validate_page_url(self, field):
        if not field.data:
            field.data = translit_text(self.title.data)


class PostForm(Form):
    title = StringField(widget=AutoFocusTextInput())
    slug = StringField()
    category_id = SelectField('Category', choices=('one', 'One'))
    text = StringField()
    draft = BooleanField()
    show_on_index = OnOffField('Show on index page')
    language = LanguageSelectField(default='eng')
