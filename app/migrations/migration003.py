from playhouse.migrate import migrate

from app import models


def m_003(migrator):
    """
    Update post text field
    """
    table_name = models.Post._meta.name
    updated_column = models.Post.post_text

    migrate(
        migrator.change_column_type(table_name, updated_column)
    )
