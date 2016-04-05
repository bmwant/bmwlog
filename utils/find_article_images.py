import os

import term

from HTMLParser import HTMLParser

from app import config
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

        
def get_images_list():
    """
    Return list of image names found in articles
    """
    all_posts = Post.select()
    parser = ImgParser()
    for post in all_posts:
        parser.feed(post.post_text)

    return parser._captured_tags

    
def show_images_statistics():
    """
    Iterate through all articles and find img tags in them
    """
    def find_missing(files):
        missing = []
        for filename in files:
            path_to_file = os.path.expanduser(
                    os.path.join(config.STATIC_FOLDER,
                                 filename.lstrip(os.path.sep)))
            if not os.path.exists(path_to_file):
                missing.append(filename)
        return missing

    all_posts = Post.select()
    parser = ImgParser()
    posts_affected = 0
    images_to_restore = 0
    for post in all_posts:
        parser.feed(post.post_text)
        if parser._captured_tags:
            images_in_post = len(parser._captured_tags)
            missing_images = len(find_missing(parser._captured_tags))
            term.write('Post #{post_id} has {images_count} images '.format(
                post_id=post.post_id,
                images_count=images_in_post
            ))
            if missing_images:
                term.writeLine('/ {missing_count} missing'.format(
                        missing_count=missing_images), term.yellow)
            else:
                term.writeLine('OK', term.green)
            parser.clear()
            posts_affected += 1
            images_to_restore += missing_images

    term.writeLine('Total posts with images %d' % posts_affected, term.bold)
    if images_to_restore:
        term.writeLine('Total images to restore %d' % images_to_restore,
                       term.red)
    else:
        term.writeLine('All posts are in good shape!', term.green)
    
    
if __name__ == '__main__':
    show_images_statistics()
