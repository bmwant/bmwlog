from peewee import *

db = MySQLDatabase('bmwlog', host='localhost', port=3306, user='root')

class UnknownFieldType(object):
    pass

class BaseModel(Model):
    class Meta:
        database = db

class Category(BaseModel):
    category_id = PrimaryKeyField(db_column='category_id')
    category_name = CharField()

    class Meta:
        db_table = 'category'

class User(BaseModel):
    user_id = PrimaryKeyField(db_column='user_id')
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    mail = CharField()
    nickname = CharField()
    user_password = CharField()
    picture = CharField(null=True)
    role = IntegerField(db_column='role_id')

    class Meta:
        db_table = 'user'

class Post(BaseModel):
    category_id = ForeignKeyField(db_column='category_id', rel_model=Category)
    date_posted = DateTimeField()
    post_id = PrimaryKeyField(db_column='post_id')
    post_text = CharField(null=True)
    title = CharField(null=True)
    user_id = ForeignKeyField(db_column='user_id', rel_model=User)

    class Meta:
        db_table = 'post'

class Tag(BaseModel):
    tag_id = PrimaryKeyField(db_column='tag_id')
    text = CharField()

    class Meta:
        db_table = 'tag'

class Tag_to_Post(BaseModel):
    post_id = ForeignKeyField(db_column='post_id', rel_model=Post)
    tag_id = ForeignKeyField(db_column='tag_id', rel_model=Tag)

    class Meta:
        db_table = 'tag_to_post'

