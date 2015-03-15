import datetime
import cgi

from bs4 import BeautifulSoup
from bottle import abort
from peewee import *
from app import db


class UnknownFieldType(object):
    pass


class BaseModel(Model):
    class Meta:
        database = db

    @classmethod
    def get_or_404(cls, *query, **kwargs):
        try:
            inst = cls.get(*query, **kwargs)
            return inst
        except DoesNotExist:
            abort(404)


class Category(BaseModel):
    category_id = PrimaryKeyField(db_column='category_id')
    category_name = CharField()

    @property
    def posts_count(self):
        return Post.get_posts().where(Post.category == self.category_id).count()


    class Meta:
        db_table = 'category'


class Role(BaseModel):
    class Meta:
        db_table = 'role'
        
    role_id = PrimaryKeyField()
    level = IntegerField(default=40)
    role = CharField(null=False)


class User(BaseModel):
    user_id = PrimaryKeyField(db_column='user_id')
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    mail = CharField(null=False, unique=True)
    nickname = CharField()
    user_password = CharField()
    picture = CharField(default='default.png')
    role = ForeignKeyField(db_column='role_id', rel_model=Role)

    @staticmethod
    def encode_password(password):
        import hashlib
        m = hashlib.md5()
        m.update(password)
        return m.hexdigest()

    @classmethod
    def create(cls, **query):
        role = Role.get(Role.role == 'user')  # default role is user
        #cls.role = role
        return super(User, cls).create(role=role, **query)

    def is_admin(self):
        return self.role.role == 'admin'

    def __repr__(self):
        return '{nickname} [{mail}]'.format(nickname=self.nickname,
                                            mail=self.mail)
    class Meta:
        db_table = 'user'


class Post(BaseModel):
    post_id = PrimaryKeyField(db_column='post_id')
    category = ForeignKeyField(db_column='category_id', rel_model=Category)
    user = ForeignKeyField(db_column='user_id', rel_model=User)

    date_posted = DateTimeField(default=datetime.datetime.now())
    date_updated = DateTimeField(default=datetime.datetime.now())

    post_text = CharField(null=True)
    title = CharField(null=True)

    likes = IntegerField(default=0)
    views = IntegerField(default=0)

    draft = BooleanField()
    deleted = BooleanField()

    def serialize(self):
        from helpers import shorten_text
        return {
            'id': self.post_id,
            'title': self.title,
            'date': self.date_posted.strftime('%d/%m/%Y'),
            'short_text': shorten_text(self.post_text)
        }

    @property
    def comments(self):
        """
        Get comments count
        """
        return 10

    def save(self, *args, **kwargs):
        post_html = self.post_text
        soup = BeautifulSoup(post_html)
        for elem in soup.select('pre > code.language-html'):
            soup[elem] = elem.replace_with(cgi.escape(elem.renderContents()))

        self.post_text = soup.decode('utf-8')
        return super(Post, self).save(*args, **kwargs)

    @classmethod
    def create(cls, **query):
        #soup = BeautifulSoup(cls.post_text)
        #for elem in soup.select('pre > code.language-html'):
        #    soup[elem] = elem.replace_with(cgi.escape(elem.renderContents()))
        #cls.post_text = soup
        return super(Post, cls).create(**query)

    class Meta:
        db_table = 'post'


    @classmethod
    def get_drafts(cls):
        """
        Return only draft posts
        """
        return cls.select().where(Post.deleted == False,
                                  Post.draft == True)

    @classmethod
    def get_deleted(cls):
        """
        Return only deleted
        """
        return cls.select().where(Post.deleted == True)

    @classmethod
    def get_posts(cls):
        """
        Get not deleted and not drafts to display in post list
        """
        return cls.select().where(Post.deleted == False,
                                  Post.draft == False)

    @classmethod
    def get_for_user(cls, user_id):
        """
        Get published posts for this specific user
        """
        return cls.select().where(Post.deleted == False,
                                  Post.draft == False,
                                  Post.user == user_id)

    def get_all(self):
        raise NotImplemented


class Photo(BaseModel):
    class Meta:
        db_table = 'photo'

    photo_id = PrimaryKeyField(db_column='photo_id')
    photo = CharField()
    desc = CharField()
    date_added = DateTimeField(default=datetime.datetime.now)


class Banner(BaseModel):
    class Meta:
        db_table = 'banner'

    banner_id = PrimaryKeyField(db_column='banner_id')
    desc = CharField()
    link = CharField()
    img = CharField()
    disabled = BooleanField(default=False)


class Quote(BaseModel):
    class Meta:
        db_table = 'quote'

    quote_id = PrimaryKeyField(db_column='quote_id')
    text = CharField(null=False)
    author = CharField(null=False)


class Tag(BaseModel):
    tag_id = PrimaryKeyField(db_column='tag_id')
    text = CharField(null=False, unique=True)

    @property
    def posts_count(self):
        """
        How many posts there are with current tag
        """
        return Tag_to_Post.select().where(Tag_to_Post.tag_id == self.tag_id).count()

    class Meta:
        db_table = 'tag'


class Tag_to_Post(BaseModel):
    post_id = ForeignKeyField(db_column='post_id', rel_model=Post)
    tag_id = ForeignKeyField(db_column='tag_id', rel_model=Tag)

    class Meta:
        db_table = 'tag_to_post'


class StreamMessage(BaseModel):
    id = PrimaryKeyField()
    date = DateTimeField(default=datetime.datetime.now)
    message = CharField()

    class Meta:
        db_table = 'stream_message'


class StaticPage(BaseModel):
    id = PrimaryKeyField()

    url = CharField(unique=True)
    date = DateTimeField(default=datetime.datetime.now)
    title = CharField()
    text = TextField()

    class Meta:
        db_table = 'static_page'


class Session(BaseModel):
    session_id = PrimaryKeyField()
    mail = CharField(null=False)
    expires = IntegerField(default=0)
    ip = CharField(null=True)
    login_date = DateTimeField(default=datetime.datetime.now)
    active = BooleanField(default=True)

    class Meta:
        db_table = 'session'


class SiteJoke(BaseModel):
    id = PrimaryKeyField()
    text = CharField(null=False)

    class Meta:
        db_table = 'site_joke'