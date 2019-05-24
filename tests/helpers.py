import os
import time
import subprocess
import docker

from utils.helpers import info, warn
from app import config
from app.helput import get_list_of_files


def run_mysql_container():
    client = docker.from_env()
    container_name = 'local-mysql'
    volume_path = os.path.join(config.PROJECT_DIR, 'tests', 'sql')
    container = client.containers.run(
        'mysql',
        name=container_name,
        auto_remove=True,
        environment={
            'MYSQL_ALLOW_EMPTY_PASSWORD': True,
        },
        detach=True,
        volumes={
            volume_path: {'bind': '/data/', 'mode': 'ro'},
        }
    )
    return container


def _retry(func, exceptions_list, retries=10):
    for _ in range(retries):
        try:
            func()
        except exceptions_list:
            info('Waiting to retry function once again...')
            time.sleep(3)
    else:
        raise RuntimeError('Failed to executed %s in %s retries' %
                           (func, retries))


def _retry_container_command(container, command, retries=10):
    er = 'Container failed to execute command'
    for i in range(retries):
        er = container.exec_run(command)
        if er.exit_code == 0:
            break
        info('Waiting for container to accept command...')
        time.sleep(2)
    else:
        raise RuntimeError('Was not able to execute command %s: %s' %
                           (command, er))


def _exec_command_locally(command, env=None):
    env = env or {}
    proc = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        env=env,
    )
    try:
        stdout, stderr = proc.communicate(timeout=15)
    except subprocess.TimeoutExpired:
        warn('Command %s took too long. Forcefully killing it' % command)
        proc.kill()
        stdout, stderr = proc.communicate()

    if proc.returncode != 0:
        raise RuntimeError('Error while running command %s: %s' %
                           (command, stdout))


def init_database_locally(database_name='test', username='', password=''):
    env = {
        'MYSQL_PWD': password
    }
    command = (
        'mysql -h localhost -u {user} '
        '-e "CREATE DATABASE IF NOT EXISTS {database};"'.format(
            user=username,
            password=password,
            database=database_name,
        )
    )
    _exec_command_locally(command, env=env)
    scripts_directory = os.path.join(config.PROJECT_DIR, 'tests', 'sql')
    sql_files = get_list_of_files(scripts_directory, '.sql')
    for filename in sql_files:
        command = (
            'mysql -v -h localhost -u {user} '
            '-D {database} < {sql_script}'.format(
                user=username,
                password=password,
                database=database_name,
                sql_script=filename,
            )
        )
        _exec_command_locally(command, env=env)


def drop_database_locally(database_name='test', username='', password=''):
    env = {
        'MYSQL_PWD': password
    }
    command = (
        'mysql -h localhost -u {user} '
        '-e "DROP DATABASE IF EXISTS {database};"'.format(
            user=username,
            password=password,
            database=database_name,
        )
    )
    _exec_command_locally(command, env=env)


def init_database_within_container(mysql_container, database_name='test'):
    info('Create database')
    _retry_container_command(
        mysql_container,
        'mysql -h localhost -e "CREATE DATABASE %s;"' % database_name
    )

    info('Fill database with test data')
    scripts_directory = os.path.join(config.PROJECT_DIR, 'tests', 'sql')
    sql_files = get_list_of_files(scripts_directory, '.sql', full_path=False)
    for filename in sql_files:
        command = '/bin/bash -c "mysql -h localhost -D %s < /data/%s"' % (
            database_name, filename)
        _retry_container_command(mysql_container, command)

    warn('Waiting for mysql to feel ok...')
    time.sleep(5)


def get_container_ip_address(container):
    client = docker.from_env()
    container_data = client.api.inspect_container(container.name)
    ip_address = container_data\
        .get('NetworkSettings')\
        .get('Networks')\
        .get('bridge')\
        .get('IPAddress')
    return ip_address


def remove_container(container):
    client = docker.from_env()
    client.api.kill(container.id)

    # No need to remove. `auto_remove` flag above is provided
    # client.api.remove_container(container.id)
