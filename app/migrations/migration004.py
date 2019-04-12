from playhouse.migrate import migrate

from app import models


def m_004(migrator):
    """
    Allow tags to be more than 20 characters
    """
    table_name = models.Tag._meta.name
    updated_column = models.Tag.text

    migrate(
        migrator.change_column_type(table_name, updated_column)
    )
