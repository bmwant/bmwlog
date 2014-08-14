from HTMLParser import HTMLParser
import bottle
from functools import wraps
from app import env


def view(tpl_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tplvars = func(*args, **kwargs)
            template = env.get_template(tpl_name)
            return template.render(**tplvars)
        return wrapper
    return decorator


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def shorten_text(text):
    text = strip_tags(text)
    if len(text) > 500:
        text = text[:500] + "..."
    return text


def postd():
    return bottle.request.forms


def post_get(name, default=''):
    return bottle.request.POST.get(name, default).strip()


def redirect(where=None):
    if where is not None:
        return bottle.redirect(where)
    back = None

    if hasattr(bottle.request.headers, 'Referer'):
        back = bottle.request.headers['Referer']
    print('refferer:', back)
    if back is not None:
        return bottle.redirect(back)
    return bottle.redirect('/')
