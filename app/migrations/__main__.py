from typing import List

from peewee import InternalError, OperationalError, Entity
from playhouse.migrate import MySQLMigrator, operation

from app import connect_database
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


def load_migrations() -> List:
    # todo (misha): add autodiscovery with an order
    from app import migrations
    migrations = [
        migrations.m_001,
        migrations.m_002,
        migrations.m_003,
        migrations.m_004,
    ]

    return migrations


def migrate_database():
    db = connect_database()
    migrator = ExtendedMySQLMigrator(db)
    migrations = load_migrations()
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
