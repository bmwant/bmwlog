# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime, timedelta
from bottle import route, request, get, post, abort
from peewee import fn, IntegrityError
from models import Post, Tag, Tag_to_Post, Category, Banner, DoesNotExist, \
    StreamMessage, Quote
from helpers import shorten_text, redirect, post_get, postd, only_ajax
from user_controller import require
from app import app, env

#todo: make as class property
def post_actuality(post):
    """
    Return sophisticated value of post actuality
    """

    cv = lambda x, y: float(x)/y if x < y else 1.0  # ceil part-value
    now_time = datetime.now()
    int_posted = (now_time - post.date_posted).total_seconds()
    int_updt = (now_time - post.date_updated).total_seconds()
    int_years = timedelta(days=365*5).total_seconds()

    act = cv(post.comments, 10)*15 + cv(post.likes, 30)*15 + \
          cv(post.views, 100)*10 + (1-cv(int_posted, int_years))*40 + \
          (1-cv(int_updt, int_years))*20

    return act

@app.get('/post')
def post_index():
    all_posts = Post.get_posts().order_by(Post.date_posted.desc())
    for item in all_posts:
        item.post_text = shorten_text(item.post_text)

    random_banner = Banner.select().order_by(fn.Rand()).first() #limit(1)[0]
    quote = Quote.select().order_by(fn.Rand()).first()
    messages = StreamMessage.select()
    #print(random_banner.desc.encode('utf-8'))

    template = env.get_template('post/index.html')
    return template.render(posts=all_posts, banner=random_banner,
                           stream_messages=messages,
                           quote=quote,
                           link_what='pstlink')


@app.get('/post/<post_id:int>')
def post_view(post_id):
    try:
        #todo: rewrite with func in Post
        post = Post.get(Post.post_id == post_id)
        if post.deleted:
            #todo: make it visible to its creator
            raise DoesNotExist
        cu = app.current_user
        if post.draft:
            if cu is not None and cu.user_id != post.user.user_id:
                raise DoesNotExist
            if cu is None:
                raise DoesNotExist
    except DoesNotExist:
        abort(404)
    tags = Tag.select().join(Tag_to_Post).where(Tag_to_Post.post_id == post_id)
    #Tweet.select().join(User).where(User.username == 'Charlie'):
    template = env.get_template('post/view.html')
    #post.update(views=post.views+1).execute() #classmethod!
    post.views += 1
    post.save()  # instance method!
    return template.render(item=post, tags=tags,
                           actuality=post_actuality(post))


@app.route('/post/add', method=['GET', 'POST'])
@require('admin')
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
                           date_posted=datetime.now(),
                           draft=False,
                           )
        if int(post_get('draft')) == 1:
            post.draft = True

        post_id = post.post_id
        post.save()
        add_new_tags(post_get('tags'), post_id)
        redirect('/post/' + str(post_id))


@app.get('/post/delete/<post_id:int>')
@require('admin')
def post_delete(post_id):
    try:
        post = Post.get(Post.post_id == post_id)
        post.deleted = True
        post.save()
        app.flash(u'Статтю видалено', 'success')
        redirect()
    except Post.DoesNotExist:
        abort(404)


@app.get('/post/renew/<post_id:int>')
@require('admin')
def post_renew(post_id):
    try:
        post = Post.get(Post.post_id == post_id)
        post.date_updated = datetime.now()
        post.save()
        app.flash(u'Стаття актуалізована')
        redirect('/post/%s' % post_id)
    except DoesNotExist:
        abort(404)


@app.get('/post/deleted')
@require('admin')
def deleted_posts():
    posts = Post.get_deleted()
    info = u'Видалені статті'
    template = env.get_template('post/list.html')
    return template.render(posts=posts, info=info)


@app.route('/post/edit/<post_id:int>', method=['GET', 'POST'])
@require('admin')
def post_edit(post_id):
    if request.method == 'GET':
        try:
            post = Post.get(Post.post_id == post_id)  #todo:get not deleted
        except Post.DoesNotExist:
            abort(404)

        all_categories = Category.select()
        tags = Tag.select().join(Tag_to_Post).where(Tag_to_Post.post_id == post_id)
        template = env.get_template('post/edit.html')
        return template.render(item=post, tags=tags, categories=all_categories)
    if request.method == 'POST':
        post = Post.get(Post.post_id == post_id)
        post.category = post_get('category_id')
        post.post_text = post_get('text')
        post.title = post_get('title')
        post.draft = bool(int(post_get('draft')))  # zero int is False
        new_tags = post_get('tags')
        old_tags = Tag.select().join(Tag_to_Post)\
            .where(Tag_to_Post.post_id == post_id)
        remove_tags(old_tags, new_tags, post_id)
        add_new_tags(new_tags, post_id)
        post.save()
        app.flash(u'Статтю успішно оновлено')
        redirect('/post/' + str(post_id))


@app.route('/category/add', method=['GET', 'POST'])
@require('admin')
def category_add():
    if request.method == 'GET':
        all_categories = Category.select()
        template = env.get_template('post/category_add.html')
        return template.render(categories=all_categories)
    if request.method == 'POST':
        new_category = Category.create(category_name=post_get('category_name'))
        app.flash(u'Нова категорія була успішно додана')
        redirect('/category/add')


@app.get('/category/<category_id:int>')
def category_list(category_id):
    """
    List all posts in current category
    """
    try:
        category = Category.get(Category.category_id == category_id)
    except DoesNotExist:
        abort(404)
    all_posts = Post.get_posts().where(Post.category == category_id).order_by(Post.date_posted.desc())
    template = env.get_template('post/list.html')
    return template.render(posts=all_posts, info=u'Статті у категорії "%s"' % category.category_name)


@app.get('/category/delete/<category_id:int>')
@require('admin')
def category_delete(category_id):
    try:
        category = Category.get(Category.category_id == category_id)
    except DoesNotExist:
        abort(404)
    try:
        category.delete_instance()
    except IntegrityError, e:
        app.flash(u'Категорія містить статті. Неможливо видалити', 'error')

    redirect('/category/add')


def add_new_tags(tags_string, post_id):
    """
    Add new tags or create connection to post with existed
    """
    tags = tags_string.split(';')
    for tag in tags:
        tg = tag.replace(' ', '')
        if not tg:
            continue
        try:
            old_tag = Tag.get(Tag.text == tag)
            try:
                conn = Tag_to_Post.get(Tag_to_Post.post_id == post_id,
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
            print("We are going to remove: %s" % old_tag.text)
            Tag_to_Post.delete().where(Tag_to_Post.post_id == post_id and \
                Tag_to_Post.tag_id == old_tag.tag_id).execute()


@app.get('/tag/<tag_id:int>')
def posts_for_tag(tag_id):
    try:
        tag = Tag.get(Tag.tag_id == tag_id)
    except DoesNotExist:
        #todo: enable logging for all these exceptions
        abort(404)
    posts = Post.get_posts().join(Tag_to_Post).where(Tag_to_Post.tag_id == tag_id)
    how = posts.count()
    if how:
        info = u'Статті, відмічені тегом "%s" (%s)' % (tag.text, how)
    else:
        info = u'Для рідкісного тега "%s" немає статтей' % tag.text
    template = env.get_template('post/list.html')
    return template.render(posts=posts, info=info)


@app.get('/like/<post_id:int>')
@only_ajax
def like(post_id):
    try:
        post = Post.get(Post.post_id == post_id)
        post.likes += 1
        post.save()
    except DoesNotExist:
        abort(404)
    return 'Ok'
