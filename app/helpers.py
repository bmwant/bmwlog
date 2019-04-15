# -*- coding: utf-8 -*-
import os
import time
import subprocess
from functools import wraps

import bottle

from app import env, config
from app.helput import unique_filename, join_all_path


def view(tpl_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tplvars = func(*args, **kwargs)
            template = env.get_template(tpl_name)
            if tplvars is not None:
                return template.render(**tplvars)
            else:
                return template.render()
        return wrapper
    return decorator


def render_template(tpl_name, *args, **kwagrs):
    """
    Render template helper function
    """
    template = env.get_template(tpl_name)
    return template.render(*args, **kwagrs)


def p_count(value):
    """
    Jinja2 custom filter to use for Peewee query count
    """
    return value.count()


def format_date(value):
    """
    Filter to format date in templates.
    """
    return value.strftime(config.DEFAULT_DATE_FORMAT)


def setup_filters(jinja_env):
    jinja_env.filters['p_count'] = p_count
    jinja_env.filters['format_date'] = format_date


def only_ajax(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if bottle.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return func(*args, **kwargs)
        return bottle.abort(404)
    return decorated


def post_slug_url_filter(config):

    regexp = r'[a-z,-]+'

    def to_python(match):
        return match

    def to_url(parts):
        return parts

    return regexp, to_python, to_url


class StripPathMiddleware(object):
    """
    Middleware for stripping trailing slashes
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, e, h):
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.app(e, h)


def postd():
    return bottle.request.forms


def post_get(name, default=None):
    form = bottle.request.POST
    value = form.getunicode(name, encoding='utf-8')
    if value is None:
        if default is None:
            raise ValueError('Post data does not contain value for %s' % name)
        return default
    return value.strip()


def post_get_checkbox(name: str) -> bool:
    form = bottle.request.POST
    value = form.getunicode(name, encoding='utf-8')
    if value == 'on':
        return True
    return False


def redirect(where=None):
    if where is not None:
        return bottle.redirect(where)
    """
    back=None
    if hasattr(bottle.request.headers, 'Referer'):
        back = bottle.request.headers['Referer']
    print('refferer:', back)
    if back is not None:
        return bottle.redirect(back)
    """
    return bottle.redirect('/')


def save_file(file_obj, where='uploaded'):
    """
    Saves file to where directory on the server
    """
    # todo: check for errors, types or file_obj properties
    folder = os.path.join(config.STATIC_FOLDER, where)
    if not os.path.exists(folder):
        os.makedirs(folder)

    new_filename = unique_filename(file_obj.filename)
    file_path = os.path.join(folder, new_filename)
    with open(file_path, 'wb') as open_file:
        open_file.write(file_obj.file.read())
    return new_filename  # returns new filename


def backup_db():
    backup_name = '{db}_backup_{date}.sql'.format(
        db=config.DB_NAME,
        date=time.strftime('%d_%m_%Y_%H-%M'))
    backup_file = join_all_path([config.ROOT_FOLDER, 'uploaded', backup_name])
    command = '/usr/bin/mysqldump -u{user} -p{password} {db}'.format(
        user=config.DB_USER, password=config.DB_PASS, db=config.DB_NAME)

    with open(backup_file, 'w') as output:
        p = subprocess.Popen(command, shell=True, stdout=output).wait()
    # todo: remove the file
    return backup_name


def root_path(path):
    root_full_path = os.path.expanduser(config.ROOT_FOLDER)
    return os.path.join(root_full_path, path)


def static_path(path):
    static_full_path = os.path.expanduser(config.STATIC_FOLDER)
    if not os.path.exists(static_full_path):
        os.makedirs(static_full_path)
    return os.path.join(static_full_path, path)
