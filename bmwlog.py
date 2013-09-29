# -*- coding: utf-8 -*-
from bottle import route, run, static_file, redirect, error, request, get, post
from jinja2 import Environment, PackageLoader
import sys
sys.path.insert(0, 'py')
from models import *

env = Environment(loader=PackageLoader('bmwlog', 'templates'))

@route('/')
def index():
    redirect('/post')

@get('/post')
#todo: category name -> template
#todo: check for correct category_id value
def post_index():
    all_posts = None
    if 'category_id' in request.query:
        all_posts = Post.select().where(Post.category_id == request.query['category_id'])
        if all_posts.count() == 0:
            template = env.get_template('info.html')
            return template.render(info=u'Жодної статті у даній категорії')
    else:
        all_posts = Post.select()
    template = env.get_template('post/index.html')
    return template.render(posts=all_posts, link_what='pstlink')

@route('/post/<id>')
def post_view(id):
    post = Post.get(Post.post_id == id)
    print post.title
    template = env.get_template('post/view.html')
    return template.render(item=post, link_what='')

@route('/post/add', method=['GET', 'POST'])
def post_add():
    if request.method == 'GET':
        all_categories = Category.select()
        template = env.get_template('post/add.html')
        return template.render(categories=all_categories)
    if request.method == 'POST':
        post = Post.create(category_id=request.forms.get('category_id'),
                           post_text=request.forms.get('text'),
                           title=request.forms.get('title'),
                           user_id=1)
        redirect('/post/' + str(post.post_id))



@route('/categories')
def categories():
    cat_list = Category.select()
    template = env.get_template('categories.html')
    return template.render(link_what="catlink", items=cat_list)

@route('/about')
def categories():
    template = env.get_template('about.html')
    return template.render(link_what='abtlink')

@route('/administration')
def categories():
    template = env.get_template('administration.html')
    return template.render(link_what='admlink')



@route('/login')
def login():
    template = env.get_template('info.html')
    return template.render(info="This is login page")

@route('/signup')
def signup():
    template = env.get_template('info.html')
    return template.render(info="This is registration page")

@error(404)
def error404(error):
    template = env.get_template('404.html')
    return template.render()

#serving static files
@route('/<folder>/<filename>')
def server_static(folder, filename):
    return static_file(filename, root='D:/coding/bmwlog/'+folder)


run(host='localhost', port=8081, debug=True)