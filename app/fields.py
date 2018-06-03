import os

from wtforms import (
    FileField,
    StringField,
    BooleanField,
    PasswordField,
)
from wtforms.widgets import HTMLString, HiddenInput, CheckboxInput

from app.models import User
from app.helpers import save_file


class UploadFileField(FileField):
    def __init__(self, label=u'', validators=None, **kwargs):
        self.target_subfolder = 'img/users'
        super(UploadFileField, self).__init__(label, validators, **kwargs)

    def process_formdata(self, valuelist):
        super(UploadFileField, self).process_formdata(valuelist)
        if self.data:
            f = save_file(self.data, self.target_subfolder)
            self.data = f

    def __call__(self, **kwargs):
        """
        Renders field with small pictogram
        """
        filepath = os.path.join('/static', self.target_subfolder,
                                self.object_data)
        img_pic = '<img class="small-icon" src="{}">'.format(filepath)
        file_input = super(UploadFileField, self).__call__(**kwargs)
        return img_pic + file_input


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


class LanguageFlagInput(HiddenInput):
    """
    Render a flag based language selection input.
    """
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        if 'value' not in kwargs:
            kwargs['value'] = field._value()
        flags_html = """
<div class="lang-icon" data-lang="eng">
  <span class="flag-icon flag-icon-gb"></span>
</div>
<div class="lang-icon" data-lang="ukr">
  <span class="flag-icon flag-icon-ua"></span>
</div>
<div class="lang-icon" data-lang="rus">
  <span class="flag-icon flag-icon-ru"></span>
</div>
"""
        input_html = '<input %s>' % self.html_params(name=field.name, **kwargs)
        html = flags_html + input_html
        return HTMLString(html)


class OnOffInput(CheckboxInput):
    def __call__(self, *args, **kwargs):
        if 'checked' not in kwargs:
            kwargs['checked'] = True
        parent_html = super(CheckboxInput, self).__call__(*args, **kwargs)
        onoff_html = '<div class="form-onoff">{}</div>'.format(parent_html)
        return HTMLString(onoff_html)


class LanguageSelectField(StringField):
    show_label = False
    widget = LanguageFlagInput()


class OnOffField(BooleanField):
    widget = OnOffInput()
