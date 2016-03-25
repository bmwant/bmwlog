from datetime import timedelta, datetime
from bottle import abort
from peewee import *
from app import app, db


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
    date_registered = DateTimeField(default=datetime.now)

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
        date_registered_str = self.date_registered.strftime('%d/%m/%Y')
        return '{nickname} [{mail}] ({date_registered})'.format(nickname=self.nickname,
                                                                mail=self.mail,
                                                                date_registered=date_registered_str)
    class Meta:
        db_table = 'user'


class Post(BaseModel):
    post_id = PrimaryKeyField(db_column='post_id')
    category = ForeignKeyField(db_column='category_id', rel_model=Category)
    user = ForeignKeyField(db_column='user_id', rel_model=User)

    date_posted = DateTimeField(default=datetime.now)
    date_updated = DateTimeField(default=datetime.now)

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
    def actuality(self):
        """
        Return sophisticated value of post actuality
        """
        cv = lambda x, y: float(x)/y if x < y else 1.0  # ceil part-value
        now_time = datetime.now()
        int_posted = (now_time - self.date_posted).total_seconds()
        int_updt = (now_time - self.date_updated).total_seconds()
        int_years = timedelta(days=365*5).total_seconds()

        comments_weight = cv(self.comments, 10)*15
        likes_weight = cv(self.likes, 30)*15
        views_weight = cv(self.views, 100)*10
        posted_weight = (1-cv(int_posted, int_years))*40  # less time passed away - higher value
        updated_weight = (1-cv(int_updt, int_years))*20

        act = comments_weight + likes_weight + views_weight + posted_weight + updated_weight

        assert act < 100

        if act < 10:
            app.log('Post %d is not relevant' % self.post_id, 'warning')
        return act

    @property
    def comments(self):
        """
        Get comments count
        """
        return 10

    def save(self, *args, **kwargs):
        return super(Post, self).save(*args, **kwargs)

    @classmethod
    def create(cls, **query):
        return super(Post, cls).create(**query)

    class Meta:
        db_table = 'post'

    @classmethod
    def search(cls, query):
        return cls.get_posts().where(Post.title.contains(query))

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
        raise NotImplementedError()

    def __str__(self):
        return '#{post_id}. {post_title}'.format(post_id=self.post_id,
                                                 post_title=self.title.encode('utf-8'))


class Photo(BaseModel):
    class Meta:
        db_table = 'photo'

    photo_id = PrimaryKeyField(db_column='photo_id')
    photo = CharField()
    desc = CharField()
    date_added = DateTimeField(default=datetime.now)


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
    date = DateTimeField(default=datetime.now)
    message = CharField()

    class Meta:
        db_table = 'stream_message'


class StaticPage(BaseModel):
    id = PrimaryKeyField()

    url = CharField(unique=True)
    date = DateTimeField(default=datetime.now)
    title = CharField()
    text = TextField()

    class Meta:
        db_table = 'static_page'


class Session(BaseModel):
    session_id = PrimaryKeyField()
    mail = CharField(null=False)
    expires = IntegerField(default=0)
    ip = CharField(null=True)
    login_date = DateTimeField(default=datetime.now)
    active = BooleanField(default=True)

    class Meta:
        db_table = 'session'


class SiteJoke(BaseModel):
    id = PrimaryKeyField()
    text = CharField(null=False)

    class Meta:
        db_table = 'site_joke'

    def __str__(self):
        return self.text[:40]
