from fabric.api import env, run, put, cd, local

import os

env.user = 'bmwant'
env.password = 'gtthrfst58'

env.hosts = ['94.45.76.62']
env.shell = "bash -c"
path = '/data/projects/bmwlog'


def stop_service():
    run('supervisorctl stop bmwlog')


def start_service():
    run('supervisorctl start bmwlog')


def deploy():
    """
    Copy all application files to the remote server. Ignores 'img' and
    'uploded' folders.
    """
    folders = ('app', 'css', 'fonts', 'js', 'templates',)
    files = ('favicon.ico', 'run.py', 'requirements.txt', 'gunicorn_settings.py',
             'nginx_bmwlog.conf', 'supervisor_bmwlog.conf')
    for fold in folders:
        put(fold, path)

    for fl in files:
        put(fl, path)
    """
    # now we're on the remote host from here on out!
    run('mkdir -p /tmp/tmp_app')
    run('mkdir -p %s' % path)
    with cd('/tmp/tmp_app'):
        run('tar zxf /tmp/tmp_app.tar.gz')
        run('cp -r %s/* %s' % (dist, path))

    # install all programs to virtual environment
    with cd(path):
        run('virtualenv venv')
        run('venv/bin/python setup.py install')
        run('venv/bin/pip install -r requirements.txt')

    """


def initialize():
    """
    function that creates virtual environment and install all needed
    modules from requirements.txt at first time
    1) create virtual environment
    2) read requirements.txt
    3) install modules
    """
    #run('mkdir ' + path + '/venv')
    with cd(path):
        run('virtualenv venv')
        #run('source venv/bin/activate')
        run('venv/bin/pip install -r requirements.txt')