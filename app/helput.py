__author__ = 'Most Wanted'
import os
import hashlib
import uuid

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
    if isinstance(path, list):
        return reduce(os.path.join, path)
    else:
        raise ValueError('Give the list of folders to join')

def unique_filename_r(file_obj):
    hash = hashlib.md5(file_obj).hexdigest()
    return


def unique_filename(filename):
    """
    The same files have the same filenames
    """
    name, ext = os.path.splitext(filename)
    new_name = uuid.uuid3(uuid.NAMESPACE_OID, filename.encode('utf-8')).hex
    return new_name + ext