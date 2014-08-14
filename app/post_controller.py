# -*- coding: utf-8 -*-
from datetime import datetime
from bottle import route, request, get, post, abort
from peewee import fn
from models import Post, Tag, Tag_to_Post, Category, Banner
from helpers import shorten_text, redirect, post_get, postd
from app import app, env


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

    random_banner = Banner.select().order_by(fn.Rand()).limit(1)[0]
    print(random_banner.desc)

    template = env.get_template('post/index.html')
    return template.render(posts=all_posts, banner=random_banner,
                           link_what='pstlink')


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
        new_tags = post_get('tags')
        old_tags = Tag.select().join(Tag_to_Post)\
            .where(Tag_to_Post.post_id == id)
        remove_tags(old_tags, new_tags, id)
        add_new_tags(new_tags, id)
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
        new_category = Category.create(category_name=post_get('category_name'))
        app.flash(u'Нова категорія була успішно додана')
        redirect('/category/add')


def add_new_tags(tags_string, post_id):
    '''
    Add new tags or create connection to post with existed
    '''
    tags = tags_string.split(';')
    for tag in tags:
        tg = tag.replace(' ', '')
        if not tg:
            continue
        try:
            old_tag = Tag.get(Tag.text == tag)
            try:
                conn = Tag_to_Post.get(Tag_to_Post.post_id == post_id, \
                    Tag_to_Post.tag_id == old_tag.tag_id)
            except Tag_to_Post.DoesNotExist:
                Tag_to_Post.create(post_id=post_id, tag_id=old_tag.tag_id)
        except Tag.DoesNotExist:
            new_tag = Tag.create(text=tag)
            Tag_to_Post.create(post_id=post_id, tag_id=new_tag.tag_id)
    return


def remove_tags(old, new, post_id):
    # todo: maybe delete unused tags
    new_tags = [nt.decode('utf-8') for nt in new.split(';')]
    #print("%s -> %s" % (new_tags[0], type(new_tags[0])))
    for old_tag in old:
        if unicode(old_tag.text) not in new_tags:
            print("We are going to remove: %s" %old_tag.text)
            Tag_to_Post.delete().where(Tag_to_Post.post_id == post_id and \
                Tag_to_Post.tag_id == old_tag.tag_id).execute()


@app.get('/tag/<id:int>')
def posts_for_tag(id):
    # todo: post list not index
    posts = Post.select().join(Tag_to_Post).where(Tag_to_Post.tag_id == id)
    template = env.get_template('post/index.html')
    return template.render(posts=posts)
