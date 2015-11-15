# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
import os
import hashlib
import uuid

from random import sample
from string import letters, digits


def get_list_of_files(directory, ext='', full_path=True):
    files = []
    for file_name in os.listdir(directory):
        if file_name.endswith(ext):
            file_path = os.path.join(directory, file_name) if full_path else file_name
            files.append(file_path)
    return files


def get_all_dirs(directory, full_path=True):
    dirs = []
    for file_name in os.listdir(directory):
        path = os.path.join(directory, file_name)
        if os.path.isdir(path):
            dirs.append(path) if full_path else dirs.append(file_name)
    return dirs


def join_all_path(path):
    # todo: make it normpath
    if isinstance(path, list):
        return reduce(os.path.join, path)
    else:
        raise ValueError('Give the list of folders to join')


def unique_filename(filename):
    """
    The same files have the same filenames
    """
    name, ext = os.path.splitext(filename)
    new_name = uuid.uuid3(uuid.NAMESPACE_OID, filename.encode('utf-8')).hex
    return new_name + ext


def generate_filename(prefix='', suffix='', length=5):
    """
    Generate random filename with given parameters
    """
    chars = letters + digits
    f_name = ''.join(sample(chars, length))
    print(f_name)
    return '{prefix}{f_name}{suffix}'.format(prefix=prefix, f_name=f_name,
                                             suffix=suffix)


def distort_filename(filename):
    """
    Generate modified filename based on the original filename
    """
    name, ext = os.path.splitext(filename)
    return '{original_name}_{appendix}{extension}'.format(original_name=name,
                                                          appendix=generate_filename(length=4),
                                                          extension=ext)


def translit_url(url_text=u''):
    """
    Generate a correct url based on static page title
    """
    url_text = url_text.lower()
    char_table = {
        u'а': 'a',
        u'б': 'b',
        u'в': 'v',
        u'г': 'h',
        u'ґ': 'g',
        u'д': 'd',
        u'е': 'e',
        u'є': 'je',
        u'ж': 'zh',
        u'з': 'z',
        u'и': 'y',
        u'і': 'i',
        u'ї': 'ji',
        u'й': 'ji',
        u'к': 'k',
        u'л': 'l',
        u'м': 'm',
        u'н': 'n',
        u'о': 'o',
        u'п': 'p',
        u'р': 'r',
        u'с': 's',
        u'т': 't',
        u'у': 'u',
        u'ф': 'f',
        u'х': 'kh',
        u'ц': 'c',
        u'ч': 'ch',
        u'ш': 'sh',
        u'щ': 'sch',
        u'ь': '',
        u'ю': 'ju',
        u'я': 'ja',
        u' ': '_'
    }

    result = ''
    for char in url_text:
        if char in char_table:
            result += char_table[char]
        elif char.isalnum():
            result += char
    return result