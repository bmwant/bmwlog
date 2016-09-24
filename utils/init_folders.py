import os

import term


BASE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                    os.path.pardir))

FOLDERS_LIST = [
    {'path': 'static/img/article', 'create': True},
    {'path': 'static/img/banners', 'create': True},
    {'path': 'static/img/gallery', 'create': True},
    {'path': 'static/img/users', 'create': True},
    {'path': 'static/img/projects'},
    {'path': 'files', 'create': True},
    {'path': 'uploaded', 'create': True},
    {'path': 'prod', 'create': True},
]


def create_folders(folders_list, base=''):
    for folder in folders_list:
        folder_path = folder['path']
        full_folder_path = os.path.join(base, folder_path)
        term.write('%s ' % full_folder_path)
        if not os.path.exists(folder_path):
            if folder.get('create'):
                os.makedirs(full_folder_path)
                term.writeLine('CREATED', term.yellow)
            else:
                term.writeLine('MISSING', term.red)
        else:
            term.writeLine('OK', term.green)


if __name__ == '__main__':
    create_folders(FOLDERS_LIST, BASE)
