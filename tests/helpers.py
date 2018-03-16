import time
import docker

from utils.helpers import info


def run_mysql_container():
    client = docker.from_env()
    container_name = 'local-mysql'
    container = client.containers.run(
        'mysql',
        name=container_name,
        auto_remove=True,
        environment={
            'MYSQL_ALLOW_EMPTY_PASSWORD': True,
        },
        detach=True,
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

    # create_tables()
    # insert_fixture_data()


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
