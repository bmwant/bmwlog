import pyclbr

import peewee

from app import models
from utils.helpers import info


def create_tables():
    module_name = 'app.models'

    module_info = pyclbr.readmodule(module_name)
    db_models = []
    for value in module_info.itervalues():
        base = value.super[0]
        if hasattr(base, 'name') and base.name == 'BaseModel':
            db_models.append((value.lineno, value.name))

    # it is important to preserve order as declared in module
    # to prevent integrity errors
    for _, model in sorted(db_models):
        model_class = getattr(models, model)
        try:
            model_class.create_table()
            info('==> Table for %s created.' % model)
        except peewee.OperationalError as e:
            if e.args[0] == 1050:
                info('==> %s already exists, skipping...' % model)
            else:
                raise e
    info('==> Database successfully initialized for %s models.' %
         len(db_models))


def insert_fixture_data():
    models.Role(
        role='user'
    ).save()
    models.User.create(
        user_id=1,
        first_name='Test',
        last_name='User',
        mail='test.user@gmail.com',
        user_password='',
        nickname='test_user',
    )
    models.Category(
        category_id=1,
        category_name='Test category',
    ).save()


if __name__ == '__main__':
    create_tables()
