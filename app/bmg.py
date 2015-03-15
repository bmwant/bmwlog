# -*- coding: utf-8 -*-
"""
Bottle generator for forms and templates based on models
"""
__author__ = 'Most Wanted'


import sys
import inspect
import peewee
from bs4 import BeautifulSoup

current_module = sys.modules[__name__]


def print_classes():
    from app import models
    for name, obj in inspect.getmembers(models, inspect.isclass):
        if obj.__module__ == models.__name__:
            print(obj)
            for field_name, field in vars(obj).iteritems():
                #print()
                if isinstance(field, peewee.FieldDescriptor):
                    print(field_name)
            break

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
        soup[elem] = elem.replace_with(cgi.escape(elem.renderContents()))
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
    soupec()
    # print_classes()