from peewee import CharField, BooleanField
from playhouse.migrate import migrate, MySQLMigrator

from app import db


migrator = MySQLMigrator(db)

slug_field = CharField(default='')
show_on_index_field = BooleanField(default=True)


with db.transaction():
    migrate(
        migrator.add_column('post', 'slug', slug_field),
        migrator.add_column('post', 'show_on_index', show_on_index_field),
    )
