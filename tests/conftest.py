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
    if hasattr(session, '_mysql_container'):
        info('\n==> Cleaning up container for a database')
        container = session._mysql_container
        remove_container(container)


@pytest.fixture
def db(request):
    # todo: reset database state here
    # todo: move initialization to `run_mysql_container_if_needed`
    session = request.session
    if hasattr(session, '_mysql_container'):
        container = session._mysql_container
        ip_address = get_container_ip_address(container)
        db_name = 'bmwlogdb_test'
        new_config_values = {
            'DB_HOST': ip_address,
            'DB_USER': 'root',
            'DB_PASS': '',
            'DB_NAME': db_name,
        }
        update_app_config(new_config_values)
        if not getattr(session, '_database_initialized'):
            init_database(container, db_name)
            session._database_initialized = True


@pytest.fixture(scope='session', autouse=True)
def run_mysq_container_if_needed(request):
    """
    Run container only if any test request database feature and command line
    flag is provided.
    """
    session = request.node
    spin_container = session.config.getoption('--spin-mysql-container')
    if not spin_container:
        return

    for item in session.items:
        if 'db' in item.fixturenames:
            info('\n==> Launching mysql container')
            session._mysql_container = run_mysql_container()
            session._database_initialized = False
            return
