import os
import sys

import pytest
from helpers import (
    info,
    init_database,
    run_mysql_container,
    remove_container,
    get_container_ip_address,
)
from app import config as app_config
from app import models

try:
    from importlib import reload
except ImportError:
    pass


sys.dont_write_bytecode = True
sys.path.append(app_config.PROJECT_DIR)


def update_app_config(config_values):
    os.environ.update(config_values)
    reload(app_config)
    # Reinitialize database connection
    reload(models)


def pytest_configure(config):
    # info('==> Create docker container for a database')
    # container = run_mysql_container()
    # ip_address = get_container_ip_address(container)
    # print('ip', ip_address)
    # db_name = 'bmwlogdb_test'
    # new_config_values = {
    #     'DB_HOST': ip_address,
    #     'DB_USER': 'root',
    #     'DB_PASS': '',
    #     'DB_NAME': db_name,
    # }
    # update_app_config(new_config_values)
    # init_database(container, db_name)
    # config._mysql_container = container
    pass


def pytest_addoption(parser):
    parser.addoption('--spin-mysql-container', action='store_true',
                     default=False,
                     help='Launch docker mysql container for a test db')


def pytest_runtest_setup(item):
    if item.config.getoption('--spin-mysql-container'):
        print('Need to spin up a container for a test')
        if 'db' in item.fixturenames:
            print('We spin a container for this test')


def pytest_unconfigure(config):
    if hasattr(config, '_mysql_container'):
        info('==> Cleaning up container for a database')
        container = config._mysql_container
        remove_container(container)


def pytest_sessionstart():
    pass


def pytest_sessionfinish():
    pass


@pytest.fixture
def db():
    print('This is a database needed for a test')
