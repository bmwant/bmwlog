import pyclbr

import term
import peewee

from app import models


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
            term.writeLine('Table for %s created.' %
                           model, term.green)
        except peewee.OperationalError as e:
            if e.args[0] == 1050:
                term.writeLine('%s already exists, skipping...' %
                               model, term.bold)
            else:
                raise e
    term.writeLine('Database successfully initialized for %s '
                   'models.' % len(db_models), term.green)


if __name__ == '__main__':
    create_tables()
