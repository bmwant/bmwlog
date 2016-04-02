import os

from app.helput import get_files_under_dir, unique_filename
from utils.find_article_images import get_images_list


def find_missing_images():
    print('Fetching images names from database...')
    images_list = get_images_list()
    images_names = map(os.path.basename, images_list)
    found = []
    print('Starting local search...')
    local_files = get_files_under_dir('/', ('.jpg', '.png', '.gif'))
    print('Found %s local images' % len(local_files))
    for local_image in local_files:
        try:
            encoded_name = unique_filename(local_image)
            if encoded_name in images_names:
                found.append((local_image, encoded_name))
        except UnicodeDecodeError as e:
            print('Error with %s, skipping...' % local_image)
    print('Found: %d images of %d' % (len(found), len(images_list)))
    return found

    
if __name__ == '__main__':
    find_missing_images()
