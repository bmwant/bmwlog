import os
import sys

from helpers import (
    info,
    init_database,
    run_mysql_container,
    remove_container,
    get_container_ip_address,
)


project_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir)
)
sys.path.append(project_dir)


def pytest_configure(config):
    info('==> Create docker container for a database')
    container = run_mysql_container()
    ip_address = get_container_ip_address(container)
    database_name = 'bmwlogdb_test'
    os.environ['DB_HOST'] = ip_address
    os.environ['DB_USER'] = 'root'
    os.environ['DB_PASS'] = ''
    os.environ['DB_NAME'] = database_name
    init_database(container, database_name)
    config._mysql_container = container


def pytest_unconfigure(config):
    info('==> Cleaning up container for a database')
    if hasattr(config, '_mysql_container'):
        container = config._mysql_container
        remove_container(container)


def pytest_sessionstart():
    pass


def pytest_sessionfinish():
    pass
