# -*- coding: utf-8 -*-
from bottle import request, abort

from app import app, env
from app.models import User, DoesNotExist, Role, Post
from app.forms import UserEditForm, SignupForm
from app.helpers import post_get, redirect, view
from functools import wraps


__all__ = (
    'require',
    'authorize',
    'login',
    'signup',
    'logout',
    'user_view',
    'my_account',
    'update_account',
)


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
    form = SignupForm(request.POST)
    if request.method == 'POST':
        if form.validate():
            try:
                user = User.get(User.mail == form.mail.data)
            except DoesNotExist:
                new_user = User.create(
                    mail=form.mail.data,
                    user_password=User.encode_password(form.password.data),
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    nickname=form.nickname.data
                )
                app.flash(u'Успішна реєстрація. Тепер ви можете увійти')
                redirect('/login')
            else:
                app.flash(u'Користувач з такою поштою уже існує')
    return template.render(form=form)


@app.get('/logout')
@authorize
def logout():
    app.logout()
    app.flash(u'Successfully logged out!')
    redirect()


@app.route('/user/<user_id:int>')
@view('user/view.html')
def user_view(user_id):
    try:
        user = User.get(User.user_id == user_id)
        user_posts = Post.get_for_user(user_id).limit(10)
        return {'user': user, 'posts': user_posts}
    except DoesNotExist:
        abort(404)


@app.get('/account')
@authorize
@view('user/account.html')
def my_account():
    user = app.current_user
    form = UserEditForm(obj=user)
    my_drafts = Post.get_drafts() \
        .where(Post.user == user.user_id) \
        .order_by(Post.date_updated.desc())
    return {'user': user, 'posts': my_drafts, 'form': form}


@app.post('/account/update')
@authorize
def update_account():
    user = app.current_user
    update_form = UserEditForm(request.POST, user)
    if update_form.validate():
        update_form.populate_obj(user)
        user.save()
        app.flash(u'Successfully updated')
    else:
        app.flash(u'Incorrect somtethisd')
    redirect('/account')  # without return redirect because of raise inside


@app.get('/user/list')
@require('admin')
def list_users():
    users = User.select().order_by(User.date_registered.desc())
    template = env.get_template('user/index.html')
    return template.render(users=users)
