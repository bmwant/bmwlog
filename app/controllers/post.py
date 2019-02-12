# -*- coding: utf-8 -*-
import json
from datetime import datetime

import six
from bottle import request, abort
from peewee import fn, IntegrityError

from app import app, env, config
from app.models import (
    Tag,
    Post,
    Tag_to_Post,
    Category,
    Quote,
    Banner,
    DoesNotExist,
    StreamMessage,
)
from app.forms import PostForm
from app.helput import shorten_text, create_slug
from app.helpers import redirect, post_get, only_ajax
from app.controllers import require


@app.get('/post')
def post_index():
    all_posts = Post.get_posts(index_only=True)\
        .order_by(Post.date_posted.desc())\
        .limit(config.POSTS_PER_PAGE)

    for item in all_posts:
        item.post_text = shorten_text(item.post_text)

    random_banner = Banner.select()\
        .where(Banner.disabled == False)\
        .order_by(fn.Rand())\
        .first()
    quote = Quote.select().order_by(fn.Rand()).first()
    messages = StreamMessage.select()

    template = env.get_template('post/index.html')
    return template.render(posts=all_posts, banner=random_banner,
                           stream_messages=messages,
                           quote=quote,
                           link_what='pstlink')


@app.get('/loadmore')
@only_ajax
def load_more():
    page = request.GET.get('page', 2)
    next_posts = Post.get_posts(index_only=True)\
        .order_by(Post.date_posted.desc())\
        .paginate(int(page), config.POSTS_PER_PAGE)
    return json.dumps([p.serialize() for p in next_posts])


@app.get('/get_slug')
@only_ajax
def get_slug_for_title():
    # To be on the safe side, WSGI suggests ISO-8859-1 (aka latin1),
    # a reversible single-byte codec that can be re-encoded with
    # a different encoding later.
    title = request.GET.title
    post_id = request.GET.get('id')
    if isinstance(title, six.binary_type):
        title = title.decode('utf-8')
    slug = create_slug(title) if title else ''
    unique_slug = Post.ensure_unique_slug(slug, post_id)
    return unique_slug


@app.get('/post/<post_id:int>')
def post_view(post_id):
    post = Post.get_or_404(Post.post_id == post_id)
    return _render_post_page(post)


@app.get('/post/<slug:slug>')
def post_view_by_slug(slug):
    post = Post.get_or_404(Post.slug == slug)
    return _render_post_page(post)


def _render_post_page(post):
    cu = app.current_user
    if post.deleted or post.draft:
        if cu is not None and \
                (cu.user_id == post.user.user_id or cu.is_admin()):
            app.log('Showing post to its creator or to admin')
        else:
            abort(404)
    template = env.get_template('post/view.html')
    post.views += 1
    post.save()
    return template.render(item=post)


@app.get('/post/publish/<post_id:int>')
def post_publish(post_id):
    p = Post.get_or_404(Post.post_id == post_id)
    p.draft = False
    p.save()
    app.flash('Post was published', 'success')
    redirect('/post/%s' % post_id)


@app.get('/new')
@app.route('/post/add', method=['GET', 'POST'])
@require('admin')
def post_add():
    form = PostForm()
    if request.method == 'GET':
        all_categories = Category.select()
        template = env.get_template('post/add.html')
        return template.render(
            form=form,
            categories=all_categories,
        )
    if request.method == 'POST':
        post = Post.create(
            category=post_get('category-id'),
            post_text=post_get('text'),
            title=post_get('title'),
            slug=post_get('slug'),
            user=app.current_user.user_id,
            date_posted=datetime.now(),
            draft=bool(int(post_get('draft'))),
            show_on_index=bool(post_get('show-on-index')),
            language=post_get('language'),
        )
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
        app.flash('Post has been deleted', 'success')
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
            post = Post.get(Post.post_id == post_id)  # todo: get not deleted
        except Post.DoesNotExist:
            abort(404)

        form = PostForm(obj=post)
        all_categories = Category.select()
        template = env.get_template('post/edit.html')
        return template.render(
            item=post,
            form=form,
            categories=all_categories,
        )
    elif request.method == 'POST':
        post = Post.get(Post.post_id == post_id)
        post.category = post_get('category-id')
        post.post_text = post_get('text')
        post.slug = post_get('slug')
        post.title = post_get('title')
        post.draft = bool(int(post_get('draft')))  # zero int is False
        post.language = post_get('language')
        post.show_on_index = bool(post_get('show-on-index'))
        post.date_updated = datetime.now()
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
    all_posts = Post.get_posts()\
        .where(Post.category == category_id).order_by(Post.date_posted.desc())
    template = env.get_template('post/list.html')
    return template.render(
        posts=all_posts,
        info=u'Статті у категорії "%s"' % category.category_name
    )


@app.get('/category/delete/<category_id:int>')
@require('admin')
def category_delete(category_id):
    try:
        category = Category.get(Category.category_id == category_id)
        try:
            category.delete_instance()
        except IntegrityError as e:
            app.flash(u'Категорія містить статті. Неможливо видалити', 'error')

        redirect('/category/add')

    except DoesNotExist:
        abort(404)


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
                tmp = Tag_to_Post.get(Tag_to_Post.post_id == post_id,
                                      Tag_to_Post.tag_id == old_tag.tag_id)
            except Tag_to_Post.DoesNotExist:
                Tag_to_Post.create(post_id=post_id, tag_id=old_tag.tag_id)
        except Tag.DoesNotExist:
            new_tag = Tag.create(text=tag)
            Tag_to_Post.create(post_id=post_id, tag_id=new_tag.tag_id)
    return


def remove_tags(old, new, post_id):
    if isinstance(new, six.binary_type):
        new = new.decode('utf-8')
    new_tags = [nt for nt in new.split(';')]
    for old_tag in old:
        if six.text_type(old_tag.text) not in new_tags:
            Tag_to_Post.delete().\
                where(Tag_to_Post.post_id == post_id,
                      Tag_to_Post.tag_id == old_tag.tag_id).execute()


@app.get('/tag/<tag_id:int>')
def posts_for_tag(tag_id):
    try:
        tag = Tag.get(Tag.tag_id == tag_id)
    except DoesNotExist:
        # todo: enable logging for all these exceptions
        abort(404)
    posts = Post.get_posts().join(Tag_to_Post).\
        where(Tag_to_Post.tag_id == tag_id)
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
        return 'Ok'
    except DoesNotExist:
        abort(404)


@app.get('/search')
def search():
    title_text = request.query.getunicode('query', default='')
    result = []
    if title_text:
        posts = Post.search(title_text)
        result = [p.serialize() for p in posts]
    return json.dumps(result)
