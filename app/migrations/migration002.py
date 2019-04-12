from peewee import CharField, BooleanField
from playhouse.migrate import migrate

from app import models


def m_002(migrator):
    """
    Add columns to post
    """
    table_name = models.Post._meta.name

    slug_field = CharField(default='')
    show_on_index_field = BooleanField(default=True)

    migrate(
        migrator.add_column(table_name, 'slug', slug_field),
        migrator.add_column(table_name, 'show_on_index', show_on_index_field),
    )
