import os
import sys

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
    info('==> Create docker container for a database')
    container = run_mysql_container()
    ip_address = get_container_ip_address(container)
    print('ip', ip_address)
    db_name = 'bmwlogdb_test'
    new_config_values = {
        'DB_HOST': ip_address,
        'DB_USER': 'root',
        'DB_PASS': '',
        'DB_NAME': db_name,
    }
    update_app_config(new_config_values)
    init_database(container, db_name)
    config._mysql_container = container


def pytest_unconfigure(config):
    if hasattr(config, '_mysql_container'):
        info('==> Cleaning up container for a database')
        container = config._mysql_container
        remove_container(container)


def pytest_sessionstart():
    pass


def pytest_sessionfinish():
    pass
