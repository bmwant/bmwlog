from app import models


def test_create_slug_for_post(db):
    new_post = models.Post.create(
        category_id=1,
        user_id=1,
        title='Very long post title',
        post_text='Post content',
    )

    new_post.save()
    assert isinstance(new_post.post_id, int)
    assert new_post.slug == 'very-long-post-title'


def test_role_is_assigned_on_user_creation(db):
    new_user = models.User.create(
        first_name='Testy',
        last_name='Userie',
        nickname='testy_userie',
        user_password='encrypted',
        mail='testy.userie@gmail.com',
    )

    new_user.save()
    assert isinstance(new_user.user_id, int)
    assert new_user.role.role == 'user'
