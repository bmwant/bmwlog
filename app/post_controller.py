# -*- coding: utf-8 -*-
from datetime import datetime
from bottle import route, request, get, post, abort
from models import Post, Tag, Tag_to_Post, Category
from helpers import shorten_text, redirect, post_get
from jinja2 import Environment, PackageLoader
from app import app, env

#retrieve all post date_posted descending
@app.get('/post')
#todo: category name -> template
#todo: check for correct category_id value
def post_index():
    all_posts = None
    if 'category_id' in request.query:
        all_posts = Post.select().where(Post.category == request.query['category_id']).order_by(Post.date_posted.desc())
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
@app.get('/post/<id:int>')
def post_view(id):
    try:
        post = Post.get(Post.post_id == id)
    except Post.DoesNotExist:
        abort(404)
    tags = Tag.select().join(Tag_to_Post).where(Tag_to_Post.post_id == id)
    #Tweet.select().join(User).where(User.username == 'Charlie'):
    template = env.get_template('post/view.html')
    return template.render(item=post, link_what='', tags=tags)

@app.route('/post/add', method=['GET', 'POST'])
def post_add():
    if request.method == 'GET':
        all_categories = Category.select()
        template = env.get_template('post/add.html')
        return template.render(categories=all_categories)
    if request.method == 'POST':
        post = Post.create(category=post_get('category_id'),
                           post_text=post_get('text'),
                           title=post_get('title'),
                           user=app.current_user.user_id,
                           date_posted=datetime.now())
        post_id = post.post_id
        add_new_tags(post_get('tags'), post_id)
        redirect('/post/' + str(post_id))


@app.get('/post/delete/<id:int>')
def post_delete(id):
    try:
        post = Post.get(Post.post_id == id)
        post.delete_instance()
        redirect()
    except Post.DoesNotExist:
        abort(404)


@app.route('/post/edit/<id:int>', method=['GET', 'POST'])
def post_edit(id):
    if request.method == 'GET':
        try:
            post = Post.get(Post.post_id == id)
        except Post.DoesNotExist:
            abort(404)

        all_categories = Category.select()
        tags = Tag.select().join(Tag_to_Post).where(Tag_to_Post.post_id == id)
        template = env.get_template('post/edit.html')
        return template.render(item=post, tags=tags,
            categories=all_categories)
    if request.method == 'POST':
        post = Post.get(Post.post_id == id)
        post.category = post_get('category_id')
        post.post_text = post_get('text')
        post.title = post_get('title')
        # TODO: add new but how about remove old tags? Huh?
        add_new_tags(post_get('tags'), id)
        post.save()
        app.flash(u'Статтю успішно оновлено')
        redirect('/post/' + str(id))


@app.route('/category/add', method=['GET', 'POST'])
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


@app.get('/tag/<id:int>')
def posts_for_tag(id):
    posts = Post.select().join(Tag_to_Post).where(Tag_to_Post.tag_id == id)
    template = env.get_template('post/index.html')
    return template.render(posts=posts)
