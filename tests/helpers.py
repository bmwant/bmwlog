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


def init_database(mysql_container, database_name='test'):
    # Wait for mysql to start
    er = 'Container failed to execute command'
    for i in range(10):
        er = mysql_container.exec_run(
            'mysql -h localhost -e "CREATE DATABASE %s;"' % database_name,
        )
        if er.exit_code == 0:
            break
        info('==> Waiting for mysql server to start...')
        time.sleep(2)
    else:
        raise RuntimeError('Was not able to start mysql: %s', er)

    info('==> Fill database with test data')

    scripts_directory = os.path.join(PROJECT_DIR, 'tests', 'sql')
    sql_files = get_list_of_files(scripts_directory, '.sql', full_path=False)
    for filename in sql_files:
        er = mysql_container.exec_run(
            '/bin/bash -c "mysql -h localhost < /data/%s"' % filename
        )

        if er.exit_code != 0:
            raise RuntimeError('Failed to apply SQL on database')


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
