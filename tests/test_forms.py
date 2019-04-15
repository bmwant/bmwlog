from dataclasses import dataclass

from app.forms import PostForm


@dataclass
class PostMock:
    text: str
    show_on_index: bool


def test_custom_name_meta():
    form = PostForm()
    assert 'name="show-on-index"' in str(form.show_on_index)


def test_custom_name_with_data_set():
    post = PostMock(text='Some text', show_on_index=False)
    form = PostForm(obj=post)
    assert 'name="show-on-index"' in str(form.show_on_index)


def test_not_checked_on_off_field():
    post = PostMock(text='Some text', show_on_index=False)
    form = PostForm(obj=post)

    assert 'checked' not in str(form.show_on_index)
    assert 'value="off"' in str(form.show_on_index)


def test_checked_on_off_field():
    post = PostMock(text='Some text', show_on_index=True)
    form = PostForm(obj=post)

    assert 'checked' in str(form.show_on_index)
    assert 'value="on"' in str(form.show_on_index)
