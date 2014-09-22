__author__ = 'Most Wanted'
import os


def get_list_of_files(directory, ext='', full_path=True):
        files = []
        for file_name in os.listdir(directory):
            if file_name.endswith(ext):
                file_path = os.path.join(directory, file_name) if full_path else file_name
                files.append(file_path)
        return files
		
		
def join_all_path(path):
    if isinstance(path, list):
        return reduce(os.path.join, path)
    else:
        raise ValueError('Give the list of folders to join')