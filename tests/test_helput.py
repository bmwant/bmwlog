# -*- coding: utf-8 -*-
import os
import pytest

from app.helput import (
    join_all_path,
    unique_filename,
    generate_filename,
    translit_text,
    create_slug,
)


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


def test_generate_filename():
    filename_length = 10
    first_filename = generate_filename(length=filename_length)
    second_filename = generate_filename(length=filename_length)

    assert first_filename != second_filename
    assert len(first_filename) == filename_length
    assert len(second_filename) == filename_length

    third_filename = generate_filename(prefix='prefix', suffix='suffix')
    assert third_filename.startswith('prefix')
    assert third_filename.endswith('suffix')


def test_translit_text():
    data_one = u'дуже довга назва з пробелом'
    expected_one = 'dyzhe_dovha_nazva_z_probelom'

    data_two = u'тут повинні бути циферки 1234-and-stay_the_same'
    expected_two = 'tyt_povunni_bytu_cuferku_1234-and-stay_the_same'

    data_three = u'всякі щ і жчш'
    expected_three = 'vsjaki_sch_i_zhchsh'

    data_four = '`~@#$%^&*()-_-+={[]};:/?,.<>'
    expected_four = '-_-'

    result_one = translit_text(data_one)
    result_two = translit_text(data_two)
    result_three = translit_text(data_three)
    result_four = translit_text(data_four)

    assert result_one == expected_one
    assert result_two == expected_two
    assert result_three == expected_three
    assert result_four == expected_four


def test_create_slug():
    assert create_slug('1234') == ''
    assert create_slug('My interesting article') == 'my-interesting-article'
    assert create_slug('The #3 number can be blank ___') == 'the--number-can-be-blank-'
    assert create_slug(u'Як побороти расову дискримінацію') == 'jak-poborotu-rasovy-duskruminaciju'


