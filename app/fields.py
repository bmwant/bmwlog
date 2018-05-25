import os

from wtforms import (
    FileField,
    StringField,
    PasswordField,
)

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


class LanguageSelectField(StringField):
    pass
