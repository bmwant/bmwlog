# -*- coding: utf-8 -*-
from bottle import route, request, response, abort
from models import User, DoesNotExist, Role, Post
from forms import UserEditForm
from app import app, env
from helpers import post_get, redirect, view, save_file
from .forms import SignupForm
from functools import wraps


def require(role):
    """
    Allows user that have at least the role to access the resource
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if app.current_user is not None:
                r = Role.get(Role.role == role)
                if app.current_user.role.level >= r.level:
                    return func(*args, **kwargs)
                app.flash(u'У Вас недостатньо прав для перегляду')
                redirect()
            app.flash(u'Увійдіть, щоб переглянути дану сторінку')
            #print(request.path)
            redirect('/login?back=' + request.path)
        return wrapper
    return decorator


def authorize(func):
    """
    User needs to be logged in
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if app.current_user is not None:
            return func(*args, **kwargs)
        app.flash(u'Увійдіть, щоб переглянути дану сторінку')
        redirect('/login?back=' + request.path)
    return wrapper


@app.route('/login', method=['GET', 'POST'])
def login():
    if 'back' in request.query:
        back = request.query['back']
    else:
        back = '/'
    if app.current_user is not None:
        app.flash(u'Вийдіть з поточної сесії, щоб увійти під іншим акаунтом')
        redirect(back)
    if request.method == 'POST':
        try:
            user = User.get(User.mail == post_get('email'))
        except DoesNotExist:
            app.flash(u'Немає такого користувача')
        else:
            if user.user_password == User.encode_password(
                    post_get('password')):
                app.flash(u'Ви успішно увійшли')
                app.login(user)
                redirect(back)
            else:
                app.flash(u'Невірний пароль')

    template = env.get_template('user/login.html')

    return template.render()


@app.route('/signup', method=['GET', 'POST'])
def signup():

    template = env.get_template('user/signup.html')
    if request.method == 'GET':
        form = SignupForm()
        return template.render(form=form)
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.validate():
            try:
                user = User.get(User.mail == form.mail.data)
            except DoesNotExist:
                new_user = User.create(mail=form.mail.data,
                                       user_password=User.encode_password(form.password.data),
                                       first_name=form.first_name.data,
                                       last_name=form.last_name.data,
                                       nickname=form.nickname.data
                )
                app.flash(u'Успішна реєстрація. Тепер ви можете увійти')
                return redirect('/login')
            else:
                app.flash(u'Користувач з такою поштою уже існує')
        return template.render(form=form)


@app.get('/logout')
@authorize
def logout():
    app.logout()
    app.flash(u'Ви успішно вийшли')
    redirect()


@app.route('/user/<user_id:int>')
@view('user/view.html')
def user_view(user_id):
    try:
        user = User.get(User.user_id == user_id)
    except DoesNotExist:
        abort(404)
    user_posts = Post.get_for_user(user_id)
    return {'user': user, 'posts': user_posts}


@app.get('/account')
@authorize
@view('user/account.html')
def my_account():
    user = app.current_user
    form = UserEditForm(obj=user)
    print(form.data)
    my_drafts = Post.get_drafts().where(Post.user == user.user_id)
    return {'user': user, 'posts': my_drafts, 'form': form}


@app.post('/account/update')
@authorize
def update_account():
    user = app.current_user
    update_form = UserEditForm(request.POST, user)
    if update_form.validate():
        #user.update(**update_form.data).execute()
        update_form.populate_obj(user)
        print(update_form.data)
        user.save()
        print(user.picture)
        app.flash(u'Дані успішно оновлено')
    else:
        app.flash(u'Incorrect somtethisd')
    redirect('/account')  # without return redirect because of raise inside


@app.get('/user/list')
@require('admin')
def list_users():
    users = User.select()
    template = env.get_template('user/index.html')
    return template.render(users=users)