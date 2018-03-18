import time
from app import models


def setup_module(module):
    # WHAT
    time.sleep(5)  # THE
    # FUCK??


def test_create_slug_for_post():
    new_post = models.Post.create(
        category_id=1,
        user_id=1,
        title='Very long post title',
        post_text='Post content',
    )

    new_post.save()
    assert isinstance(new_post.post_id, int)
    assert new_post.slug == 'very-long-post-title'
