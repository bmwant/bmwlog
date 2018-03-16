import os
import sys

from helpers import (
    info,
    run_mysql_container,
    remove_container,
    get_container_ip_address,
)


project_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir)
)
sys.path.append(project_dir)


def pytest_configure(config):
    info('==> Creating test database')
    container = run_mysql_container()
    ip_address = get_container_ip_address(container)
    os.environ['DB_HOST'] = ip_address
    os.environ['DB_USER'] = 'root'
    config._mysql_container = container


def pytest_unconfigure(config):
    info('==> Removing database')
    if hasattr(config, '_mysql_container'):
        container = config._mysql_container
        remove_container(container)


def pytest_sessionstart():
    print('Session start is called')


def pytest_sessionfinish():
    print('Session finish is called')
