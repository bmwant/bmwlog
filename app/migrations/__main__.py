from peewee import CharField, BooleanField
from playhouse.migrate import migrate, MySQLMigrator

from app import models, connect_database


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
            m(migrator)


if __name__ == '__main__':
    migrate_database()
