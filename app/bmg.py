# -*- coding: utf-8 -*-
"""
Bottle generator for forms and templates based on models
"""
__author__ = 'Most Wanted'

import os
import sys
import inspect
import peewee
import wtforms
import argparse
import importlib
from shutil import copyfile
from bs4 import BeautifulSoup
from jinja2 import Template


current_module = sys.modules[__name__]


PEEWEE_TO_WTFORMS = {
    peewee.CharField: wtforms.StringField,
    peewee.IntegerField: wtforms.IntegerField,
    peewee.BooleanField: wtforms.BooleanField,
    peewee.DateTimeField: wtforms.DateTimeField
}


class BMG:
    """

    """
    def __init__(self, command):
        print('You are trying to do %s' % command)
        if command == 'list':
            self.list_models()
        elif command == 'create':
            pass
        else:
            raise ValueError('Incorrect command')

    def create_files(self):
        views_header = 'from models import *\n' \
                       'from user_controller import require\n' \
                       'from app import app\n'

        forms_header = '# -*- coding: utf-8 -*-\n' \
                       'import wtforms\n'

        if not os.path.exists('gen_forms.py'):
            with open('gen_forms.py', 'w') as fout:
                fout.writelines(forms_header)

        if not os.path.exists('gen_views.py'):
            with open('gen_views.py', 'w') as fout:
                fout.writelines(views_header)

    def list_models(self, module_name='models'):
        import pyclbr
        module = module_name
        m = pyclbr.readmodule(module)
        print('Models in %s module:' % module_name)
        counter = 1
        for value in m.itervalues():
            if value.module == module:
                base = value.super[0]
                if hasattr(base, 'name') and base.name == 'BaseModel':
                    print('[%s]: %s' % (counter, value.name))
                    counter += 1

class ViewCreator():
    template = """
@app.route('/{{ view_name }}_admin', method=['GET', 'POST'])
@require('admin')
def {{ view_name }}_admin():
    template = env.get_template('gen_views/{{ view_name }}_admin.html')
    if request.method == 'GET':
        items = {{ peewee_model }}.select()
        return template.render(items)
"""

    def __init__(self, name):
        self.name = name
        self.peewee_model = name.title()

    def write(self):
        t = Template(self.template)
        bottle_view = t.render(view_name=self.name,
                               peewee_model=self.peewee_model)
        with open('gen_views.py', 'a') as fout:
            fout.writelines(bottle_view)

        self.create_template()

    def create_template(self):
        templates_dir = '../templates'
        copyfile('{0}/blueprint.html'.format(templates_dir),
                 '{0}/gen_views/{1}_admin.html'.format(templates_dir, self.name))


class Jumbotron():
    template = """
class {{ class_name }}(wtforms.Form):
    {% for field in class_fields %}{{ field.name }} = wtforms.{{ field.type_}}()
    {% endfor %}
"""

    def __init__(self, name):
        self.name = name
        self.fields = []

    def add_field(self, field_name, field_type):
        self.fields.append({'name': field_name, 'type_': field_type})

    def render(self):
        t = Template(self.template)
        return t.render(class_name=self.name, class_fields=self.fields)

    def write(self):
        with open('created_forms.py', 'a') as fout:
            fout.writelines(self.render())

def form_creator(obj):
    new_form_name = obj.__name__ + 'Form'  # e.g. UserForm
    new_view_name = obj.__name__.lower()
    #new_form_class = type(new_form_name, (wtforms.Form, ), {})
    j = Jumbotron(new_form_name)
    for field_name, field in vars(obj).iteritems():
        if isinstance(field, peewee.FieldDescriptor):
            for key in PEEWEE_TO_WTFORMS.iterkeys():
                if key is type(field.field):
                    j.add_field(field_name, PEEWEE_TO_WTFORMS[key].__name__)
                    #setattr(new_form_class, field_name, PEEWEE_TO_WTFORMS[key])
                    #print('%s -> %s' % (field.field, PEEWEE_TO_WTFORMS[key]))
    #print(j.render())
    j.write()
    v = ViewCreator(new_view_name)
    v.write()


def class_serializer(class_):
    pass


def print_classes():
    from app import models

    for name, obj in inspect.getmembers(models, inspect.isclass):
        if obj.__module__ == models.__name__:
            print(obj.__name__)


#clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)

def soupec():
    html = """<p> </p>

<h3>Статичні файли на продакшені</h3>

<p>На продакшен-машині видачею статичних файлів має займатися nginx. Для цього потрібно вибрати папку, де вони будуть зберігатися і задати її в <strong>settings.py</strong></p>

<pre>
 <code class="language-python">STATIC_ROOT = '/path/to/project/static'</code></pre>

<p>Оскільки в шаблонах використовуються директиви виду</p>

<pre>
 <code class="language-html">{% load staticfiles %} <img src="{% static 'images/example.jpg' %}" /></code>
 <code class="language-html">virtualenv=/project/virtual/environment env=DJANGO_SETTINGS_MODULE=project.production_settings</code>
 </pre>

<pre>
 <img src="'www'" />
 </pre>

<p>то після введення</p>

<pre>
 <code class="language-bash">python manage.py collectstatic</code></pre>
"""
    import cgi
    soup = BeautifulSoup(html)
    for elem in soup.select('pre > code.language-html'):
        new_content = cgi.escape(elem.renderContents())
        elem.string = new_content
        print(elem.children)
        #elem.contents = new_content

    print(soup)

    """
    for pre in soup.find_all('pre'):
        contents_code = pre.findAll('code', class_=u'language-html')
        if contents_code:
            for part in contents_code:
                print(part)
                #print(dir(part))
                part.replace_with('Replaced')
                print(part)


    print(html)

        if pre.children:
            for code in pre.children:
                print(code)
                if code.parent['class'] == u'language-html':
                    pass
    """

if __name__ == '__main__':
    #soupec()
    #print_classes()
    #parser = argparse.ArgumentParser()
    #parser.add_argument('command', help='What to do? list, create [modelname]',
    #                    type=str)
    #args = parser.parse_args()
    #bmg = BMG(args.command)
    bmg = BMG('list')