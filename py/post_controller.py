# -*- coding: utf-8 -*-
from datetime import datetime
from bottle import route, redirect, request, get, post
from models import Post, Tag, Tag_to_Post, Category
from helpers import shorten_text
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('bmwlog', 'templates'))

#retrieve all post date_posted descending
@get('/post')
#todo: category name -> template
#todo: check for correct category_id value
def post_index():
    all_posts = None
    if 'category_id' in request.query:
        all_posts = Post.select().where(Post.category_id == request.query['category_id']).order_by(Post.date_posted.desc())
        if all_posts.count() == 0:
            template = env.get_template('info.html')
            return template.render(info=u'Жодної статті у даній категорії')
    else:
        all_posts = Post.select().order_by(Post.date_posted.desc())
    for item in all_posts:
        item.post_text = shorten_text(item.post_text)
    template = env.get_template('post/index.html')
    return template.render(posts=all_posts, link_what='pstlink')

#retrieve post
@get('/post/<id:int>')
def post_view(id):
    post = Post.get(Post.post_id == id)
    tags = Tag.select().join(Tag_to_Post).where(Tag_to_Post.post_id == id)
    #Tweet.select().join(User).where(User.username == 'Charlie'):
    template = env.get_template('post/view.html')
    return template.render(item=post, link_what='', tags=tags)

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
                           user_id=1,
                           date_posted=datetime.now())
        post_id = post.post_id
        add_new_tags(request.forms.get('tags'), post_id)
        redirect('/post/' + str(post_id))


@route('/category/add', method=['GET', 'POST'])
def category_add():
    if request.method == 'GET':
        all_categories = Category.select()
        template = env.get_template('post/category_add.html')
        return template.render(categories=all_categories)
    if request.method == 'POST':
        new_category = Category.create(category_name=request.forms.get('category_name'))
        redirect('/category/add')


#add new tags or create connection to post with existed
def add_new_tags(tags_string, post_id):
    tags = tags_string.split(';')
    for tag in tags:
        try:
            old_tag = Tag.get(Tag.text == tag)
            Tag_to_Post.create(post_id=post_id, tag_id=old_tag.tag_id)
        except Tag.DoesNotExist:
            new_tag = Tag.create(text=tag)
            Tag_to_Post.create(post_id=post_id, tag_id=new_tag.tag_id)
    return


@get('/tag/<id:int>')
def posts_for_tag(id):
    posts = Post.select().join(Tag_to_Post).where(Tag_to_Post.tag_id == id)
    template = env.get_template('post/index.html')
    return template.render(posts=posts)