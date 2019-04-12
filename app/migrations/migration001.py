from peewee import CharField
from playhouse.migrate import migrate

from app import models


def m_001(migrator):
    """
    Add language column to post
    """
    table_name = models.Post._meta.name

    language_field = CharField(null=False, default='ukr')

    migrate(
        migrator.add_column(table_name, 'language', language_field),
    )
