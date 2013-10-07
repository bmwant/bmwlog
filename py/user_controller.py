from bottle import route
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('bmwlog', 'templates'))

@route('/login')
def login():
    template = env.get_template('user/login.html')
    return template.render()

@route('/signup')
def signup():
    template = env.get_template('user/signup.html')
    return template.render()