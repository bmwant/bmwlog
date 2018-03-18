import os
import time
import docker

from utils.helpers import info
from app.config import PROJECT_DIR
from app.helput import get_list_of_files


def run_mysql_container():
    client = docker.from_env()
    container_name = 'local-mysql'
    volume_path = os.path.join(PROJECT_DIR, 'tests', 'sql')
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


def _retry_container_command(container, command, retries=10):
    er = 'Container failed to execute command'
    for i in range(retries):
        er = container.exec_run(command)
        if er.exit_code == 0:
            break
        info('==> Waiting for container to accept command...')
        time.sleep(2)
    else:
        raise RuntimeError('Was not able to execute command %s: %s' %
                           (command, er))


def init_database(mysql_container, database_name='test'):
    info('==> Create database')
    _retry_container_command(
        mysql_container,
        'mysql -h localhost -e "CREATE DATABASE %s;"' % database_name
    )

    info('==> Fill database with test data')
    scripts_directory = os.path.join(PROJECT_DIR, 'tests', 'sql')
    sql_files = get_list_of_files(scripts_directory, '.sql', full_path=False)
    for filename in sql_files:
        command = '/bin/bash -c "mysql -h localhost -D %s < /data/%s"' % (
            database_name, filename)
        _retry_container_command(mysql_container, command)


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
