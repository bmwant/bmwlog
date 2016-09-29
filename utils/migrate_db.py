# -*- coding: utf-8 -*-
from peewee import CharField
from playhouse.migrate import migrate, MySQLMigrator


from app import db
from app import models


def v1(migrator):
    languages = (
        ('eng', 'English'),
        ('rus', u'Русский'),
        ('ukr', u'Українська'),
    )
    language_field = CharField(default=languages[-1], choices=languages)

    table_name = models.Post._meta.name
    migrate(
        migrator.drop_column(table_name, 'language'),
        migrator.add_column(table_name, 'language', language_field),
    )


def migrate_database():
    migrator = MySQLMigrator(db)
    v1(migrator)


if __name__ == '__main__':
    migrate_database()
