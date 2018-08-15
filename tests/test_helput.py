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


def test_unique_filename_works_for_unicode():
    result = unique_filename(u'should_be_fine.jpg')
    assert isinstance(result, str)
    assert result.endswith('.jpg')


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

    assert create_slug('ssaaff 1 1 ssdd') == 'ssaaff-1-1-ssdd'
    assert create_slug('My interesting article') == 'my-interesting-article'
    assert create_slug('single    dash  only') == \
        'single-dash-only'
    assert create_slug('The #3 number ___') == 'the-3-number'
    assert create_slug(u'Як побороти расову дискримінацію') == \
        'jak-poborotu-rasovy-duskruminaciju'
    assert create_slug(' no leading or trailing _ _ ') == \
        'no-leading-or-trailing'


def test_slug_russian_special():
    assert create_slug(u'ёЁъЪэЭ') == 'eeee'
    assert create_slug(u'иИйЙьЬ') == 'uujiji'


def test_slug_numbers_should_be_present():
    assert create_slug('1234') == '1234'
    assert create_slug('Notes. Part #1') == 'notes-part-1'
    assert create_slug('Notes. Part #2') == 'notes-part-2'
    assert create_slug('42 is the answer') == '42-is-the-answer'
    assert create_slug('Celebrate 4 of July') == 'celebrate-4-of-july'
