from peewee import CharField, BooleanField
from peewee import InternalError, OperationalError, Entity
from playhouse.migrate import migrate, MySQLMigrator, operation

from app import models, connect_database
from utils.helpers import info, warn, note


class ExtendedMySQLMigrator(MySQLMigrator):
    @operation
    def change_column_type(self, table, new_field):
        # ALTER TABLE <table_name> MODIFY <col_name> VARCHAR(65353);
        ctx = self.make_context()
        field_ddl = new_field.ddl(ctx)
        change_ctx = (self
                      .make_context()
                      .literal('ALTER TABLE ')
                      .sql(Entity(table))
                      .literal(' MODIFY ')
                      .sql(field_ddl))
        return change_ctx


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


def m_003(migrator):
    table_name = models.Post._meta.name
    updated_column = models.Post.post_text

    migrate(
        migrator.change_column_type(table_name, updated_column)
    )


def migrate_database():
    db = connect_database()
    migrator = ExtendedMySQLMigrator(db)
    migrations = [
        m_001,
        m_002,
        m_003,
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
