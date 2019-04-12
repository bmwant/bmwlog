import os
import sys

import pytest

from app import models
from app import config as app_config
from .helpers import (
    info,
    init_database_locally,
    drop_database_locally,
    init_database_within_container,
    run_mysql_container,
    remove_container,
    get_container_ip_address,
)


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
    # https://docs.pytest.org/en/latest/_modules/_pytest/hookspec.html
    pass


def pytest_addoption(parser):
    parser.addoption('--spin-mysql-container', action='store_true',
                     default=False,
                     help='Launch docker mysql container for a test db')


def pytest_runtest_setup(item):
    pass


def pytest_unconfigure(config):
    pass


def pytest_sessionstart():
    pass


def pytest_sessionfinish(session):
    if not getattr(session, 'TEST_DB_NAME', False):
        return

    # close all connections
    models.db.close()

    if hasattr(session, '_mysql_container'):
        info('\n==> Cleaning up container for a database')
        container = session._mysql_container
        remove_container(container)
    else:
        info('\n==> Removing test database')
        drop_database_locally(session.TEST_DB_NAME,
                              username=app_config.DB_USER,
                              password=app_config.DB_PASS)


@pytest.fixture
def db(request):
    session = request.session
    if hasattr(session, '_mysql_container'):
        print('Skip cleaning state')
        return

    info('\n==> Reset database state for a test')
    init_database_locally(session.TEST_DB_NAME,
                          username=app_config.DB_USER,
                          password=app_config.DB_PASS)


@pytest.fixture(scope='session', autouse=True)
def init_database_if_needed(request):
    """
    Run container only if any test request database feature and command line
    flag is provided.
    """
    session = request.node
    spin_container = session.config.getoption('--spin-mysql-container')

    for item in session.items:
        if 'db' in item.fixturenames:
            break
    else:
        return

    session.TEST_DB_NAME = 'bmwlogdb_test'
    if spin_container:
        info('\n==> Launching mysql container')
        container = run_mysql_container()
        session._mysql_container = container
        ip_address = get_container_ip_address(container)
        database_config = {
            'DB_HOST': ip_address,
            'DB_USER': 'root',
            'DB_PASS': '',
            'DB_NAME': session.TEST_DB_NAME,
        }
        update_app_config(database_config)
        init_database_within_container(container, session.TEST_DB_NAME)
    else:
        database_config = {
            'DB_HOST': 'localhost',
            'DB_NAME': session.TEST_DB_NAME,
        }
        update_app_config(database_config)
        init_database_locally(session.TEST_DB_NAME,
                              username=app_config.DB_USER,
                              password=app_config.DB_PASS)
