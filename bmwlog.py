from bottle import route, run, static_file, redirect, error, request
from jinja2 import Environment, PackageLoader
import sys
sys.path.insert(0, 'py')
from models import *

env = Environment(loader=PackageLoader('bmwlog', 'templates'))

@route('/')
def index():
    redirect('/post')

@route('/post')
def post_index():
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
        template = env.get_template('post/add.html')
        return template.render()
    if request.method == 'POST':
        post = Post.create(category=1, post_text=request.forms.get('text'), title=request.forms.get('title'), user_id=1)
        redirect('/post/' + str(post.post_id))



@route('/categories')
def categories():
    template = env.get_template('categories.html')
    return template.render(link_what="catlink")

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
    return "200 ok"

@route('/signup')
def signup():
    return "200 ok"

@error(404)
def error404(error):
    template = env.get_template('404.html')
    return template.render()

#serving static files
@route('/<folder>/<filename>')
def server_static(folder, filename):
    return static_file(filename, root='D:/coding/blogbottle/'+folder)


run(host='localhost', port=8081)