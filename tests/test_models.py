# -*- coding: utf-8 -*-
from app import models


def test_create_slug_for_post(db):
    new_post = models.Post.create(
        category_id=1,
        user_id=1,
        title='Very long post title',
        post_text='Post content',
    )

    assert isinstance(new_post.post_id, int)
    assert new_post.slug == 'very-long-post-title'


def test_ensure_unique_slug_return_same(db):
    slug = 'unique-post-slug'
    assert models.Post.ensure_unique_slug(slug) == slug


def test_ensure_unique_slug_already_exists(db):
    post = models.Post.create(
        category_id=1,
        user_id=1,
        title='Test post slug',
        post_text='Post content',
    )

    slug = 'test-post-slug'
    assert post.slug == 'test-post-slug'

    new_slug = models.Post.ensure_unique_slug(slug)
    assert new_slug != slug


def test_crete_different_slugs_for_same_titles(db):
    post1 = models.Post.create(
        category_id=1,
        user_id=1,
        title='Just title',
        post_text='Just text',
    )

    post2 = models.Post.create(
        category_id=1,
        user_id=1,
        title='Just title',
        post_text='Just text',
    )

    assert post1.slug != post2.slug


def test_role_is_assigned_on_user_creation(db):
    new_user = models.User.create(
        first_name='Testy',
        last_name='Userie',
        nickname='testy_userie',
        user_password='encrypted',
        mail='testy.userie@gmail.com',
    )

    assert isinstance(new_user.user_id, int)
    assert new_user.role.role == 'user'


def test_encode_password():
    p1 = models.User.encode_password('regular-string')
    assert isinstance(p1, str)

    p2 = models.User.encode_password(u'юникод')
    assert len(p2) == 32

    p3 = models.User.encode_password(b'bytes-here')
    assert p3 != p2
