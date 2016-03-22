from HTMLParser import HTMLParser

from app.models import Post


class ImgParser(HTMLParser):
    def __init__(self):
        self._captured_tags = []
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self._captured_tags.append(self._filter_attrs(attrs, 'src'))

    def _filter_attrs(self, attrs, filter_attr):
        for attr_name, attr_value in attrs:
            if attr_name == filter_attr:
                return attr_value

    def clear(self):
        self._captured_tags = []


if __name__ == '__main__':
    """
    Iterate through all articles and find img tags in them
    """
    all_posts = Post.select()
    parser = ImgParser()
    posts_affected = 0
    images_to_restore = 0
    for post in all_posts:
        parser.feed(post.post_text)
        if parser._captured_tags:
            images_in_post = len(parser._captured_tags)
            print('Post #{post_id} has {images_count} images'.format(
                post_id=post.post_id,
                images_count=images_in_post
            ))
            parser.clear()
            posts_affected += 1
            images_to_restore += images_in_post

    print('Total posts affected %d' % posts_affected)
    print('Total images to restore %d' % images_to_restore)
