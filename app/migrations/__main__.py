from peewee import CharField, BooleanField
from peewee import InternalError, OperationalError
from playhouse.migrate import migrate, MySQLMigrator

from app import models, connect_database
from utils.helpers import info, warn, note


def m_001(migrator):
    table_name = models.Post._meta.name

    language_field = CharField(null=False, default='ukr')

    migrate(
        migrator.add_column(table_name, 'language', language_field),
    )


def m_002(migrator):
    table_name = models.Post._meta.name

    slug_field = CharField(default='')
    show_on_index_field = BooleanField(default=True)

    migrate(
        migrator.add_column(table_name, 'slug', slug_field),
        migrator.add_column(table_name, 'show_on_index', show_on_index_field),
    )


def migrate_database():
    db = connect_database()
    migrator = MySQLMigrator(db)
    migrations = [
        m_001,
        m_002,
    ]
    for m in migrations:
        with db.transaction():
            try:
                info('Running migration %s...' % m.__name__)
                m(migrator)
            except (InternalError, OperationalError) as e:
                warn('Seems like migration %s has been already applied: %s' %
                     (m.__name__, e))
            else:
                note('Successfully applied %s migration' % m.__name__)


if __name__ == '__main__':
    migrate_database()
