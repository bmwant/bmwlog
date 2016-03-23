from app.helput import get_files_under_dir, unique_filename


def locate_():
    for ff in get_files_under_dir('/home/vagrant/workspace/bmwlog', '.jpg'):
        print(ff, unique_filename(ff))


if __name__ == '__main__':
    locate_()
