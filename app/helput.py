__author__ = 'Most Wanted'
import os

def get_list_of_files(directory, ext='', full_path=True):
        files = []
        for file in os.listdir(directory):
            if file.endswith(ext):
                file_path = os.path.join(directory, file) if full_path else file
                files.append(file_path)
        return files