import os
import pytest

from app.helput import join_all_path, unique_filename


def test_join_all_path():
    list_of_folders = ('dir1', 'dir2', 'dir3')
    result = join_all_path(list_of_folders)
    assert result == 'dir1/dir2/dir3'

    with pytest.raises(ValueError):
        join_all_path('not a list')


def test_unique_filename():
    original_filename = 'filename.txt'
    _, original_ext = os.path.splitext(original_filename)
    result = unique_filename(original_filename)
    result_name, result_ext = os.path.splitext(result)

    assert result != original_filename
    assert result_ext == original_ext
    # UUID is a string from 32 hexadecimal digits
    assert len(result_name) == 32
