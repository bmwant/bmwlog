from bottle import route, request, redirect
from jinja2 import Environment, PackageLoader
from models import User
from app import app, env

@app.route('/login', method=['GET', 'POST'])
def login():
  template = env.get_template('user/login.html')
  if request.method == 'POST':
      app.flash('Login ok')
      
  return template.render()

@app.route('/signup', method=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        template = env.get_template('user/signup.html')
        return template.render()
    if request.method == 'POST':
        new_user = User.create(first_name=request.forms.get('fname'),
                           last_name=request.forms.get('lname'),
                           nickname=request.forms.get('nickname'),
                           user_password=User.encode_password(request.forms.get('password')),
                           mail=request.forms.get('email'))
        return redirect('/')
