def m_003(migrator):
    table_name = models.Post._meta.name
    updated_column = models.Post.post_text

    migrate(
        migrator.change_column_type(table_name, updated_column)
    )
