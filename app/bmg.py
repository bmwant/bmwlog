# -*- coding: utf-8 -*-
"""
Bottle generator for forms and templates based on models
"""
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


FORMS_FILE = 'gen_forms.py'
VIEWS_FILE = 'gen_views.py'

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

    def __call__(self, command, model_name):
        if command == 'create':
            self.generate_model_data(model_name)
        else:
            raise ValueError('What you are trying to do?')

    def create_files(self):

        if not os.path.exists(FORMS_FILE):
            copyfile('bmg/forms_header.py', 'gen_forms.py')

        if not os.path.exists(VIEWS_FILE):
            copyfile('bmg/views_header.py', 'gen_views.py')

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

    def generate_view(self, view_name, model_name):
        v = ViewCreator(view_name, model_name)
        v.write()

    def _create(self, obj):
        print('Creating all for %s' % obj.__name__)
        new_form_name = obj.__name__ + 'Form'  # e.g. UserForm
        new_view_name = obj.__name__.lower()

        # new_form_class = type(new_form_name, (wtforms.Form, ), {})
        j = Jumbotron(new_form_name)
        for field_name, field in vars(obj).iteritems():
            if isinstance(field, peewee.FieldDescriptor):
                for key in PEEWEE_TO_WTFORMS.iterkeys():
                    if key is type(field.field):
                        j.add_field(field_name,
                                    PEEWEE_TO_WTFORMS[key].__name__)
        j.write()
        self.generate_view(new_view_name, obj.__name__)

    def generate_model_data(self, model_name=None):
        self.create_files()

        from app import models

        for name, obj in inspect.getmembers(models, inspect.isclass):
            if obj.__module__ == models.__name__:
                if model_name is None:
                    self._create(obj)
                elif obj.__name__ == model_name:
                    self._create(obj)
                    break


class ViewCreator(object):
    template = """


@app.route('/{{ view_name }}_admin', method=['GET', 'POST'])
@require('admin')
def {{ view_name }}_admin():
    template = env.get_template('gen_views/{{ view_name }}_admin.html')
    form = {{ peewee_model }}Form(request.POST)
    items = {{ peewee_model }}.select()
    if request.method == 'POST':
        if form.validate():
            new_item = SiteJoke.create(**form.data)
            form = {{ peewee_model }}Form()
    return template.render(items=items, form=form)


@app.route('/{{ view_name }}_admin/edit/<{{ view_name }}_id:int>', method=['GET', 'POST'])
def {{ view_name }}_edit({{ view_name }}_id):
    item = {{ peewee_model }}.get_or_404({{ peewee_model }}.id == {{ view_name }}_id)
    if request.method == 'GET':
        return json.dumps(item, cls=PeeweeModelEncoder)

    form = {{ peewee_model }}Form(request.POST)
    if form.validate():
        for attr, value in form.data.iteritems():
            setattr(item, attr, value)
        item.save()
        redirect('/{{ view_name }}_admin')

    items = {{ peewee_model }}.select()
    template = env.get_template('gen_views/{{ view_name }}_admin.html')
    return template.render(items=items, form=form)


@app.get('/{{ view_name }}_admin/delete/<{{ view_name }}_id:int>')
@require('admin')
def {{ view_name }}_delete({{ view_name }}_id):
    item = {{ peewee_model }}.get({{ peewee_model }}.id == {{ view_name }}_id)
    item.delete_instance()
    return json.dumps({
        'status': 'success',
        'message': 'Item was deleted'
    })
"""

    def __init__(self, name, peewee_model):
        self.name = name
        self.peewee_model = peewee_model

    def write(self):
        t = Template(self.template)
        bottle_view = t.render(view_name=self.name,
                               peewee_model=self.peewee_model)
        with open(VIEWS_FILE, 'a') as fout:
            fout.writelines(bottle_view)

        self.create_template()

    def create_template(self):
        templates_dir = '../templates'
        copyfile('{0}/blueprint.html'.format(templates_dir),
                 '{0}/gen_views/{1}_admin.html'.format(templates_dir, self.name))


class Jumbotron(object):
    template = """


class {{ class_name }}(Form):
    {% for field in class_fields %}{{ field.name }} = wtforms.{{ field.type_}}(validators=[validators.InputRequired()])
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
        with open(FORMS_FILE, 'a') as fout:
            fout.writelines(self.render())




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
    bmg('create', 'SiteJoke')
    #bmg.generate_view('sitejoke', 'SiteJoke')
