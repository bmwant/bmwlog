# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
import os
import hashlib
import uuid
import collections

from random import sample
from string import letters, digits


def get_list_of_files(directory, ext='', full_path=True):
    """
    Return list of files in directory specified
    :param directory: path to directory you want to perform search in. Not
    work with nested directories, just files that are present directly here
    :param ext: if set then only files with this extension will be matched
    :param full_path: if True that full path for each file will be as result
    :return: list of files that matched query
    """
    files = []
    for file_name in os.listdir(directory):
        if file_name.endswith(ext):
            file_path = os.path.join(directory, file_name) if full_path else file_name
            files.append(file_path)
    return files


def get_files_under_dir(directory, ext='', case_sensitive=False):
    """
    Perform recursive search in directory to match files with one of the
    extensions provided
    :param directory: path to directory you want to perform search in.
    :param ext: list of extensions of simple extension for files to match
    :param case_sensitive: is case of filename takes into consideration
    :return: list of files that matched query
    """
    if isinstance(ext, (list, tuple)):
        allowed_exensions = ext
    else:
        allowed_exensions = [ext]

    if not case_sensitive:
        allowed_exensions = map(str.lower, allowed_exensions)

    result = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            check_filename = filename if case_sensitive else filename.lower()
            if any(map(check_filename.endswith, allowed_exensions)):
                result.append(filename)
    return result


def get_all_dirs(directory, full_path=True):
    dirs = []
    for file_name in os.listdir(directory):
        path = os.path.join(directory, file_name)
        if os.path.isdir(path):
            dirs.append(path) if full_path else dirs.append(file_name)
    return dirs


def join_all_path(path):
    # todo: make it normpath
    if isinstance(path, (list, tuple)):
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
