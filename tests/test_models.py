from app.models import Post


def test_create_slug_for_post():
    new_post = Post.create(
        category_id=11,
        user_id=11,
        title='Very long post title',
        post_text='Post content',
    )

    new_post.save()
    assert isinstance(new_post.post_id, int)
    assert new_post.slug == 'very-long-post-title'
