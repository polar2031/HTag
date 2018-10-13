import os
import shutil
import platform
import subprocess


import send2trash


class PathAlreadyExistException(Exception):
    pass


class PathNotExistException(Exception):
    pass


# one document stands for one work
class Document:
    def __init__(self, document_path):
        if not os.path.exists(document_path):
            raise PathNotExistException
        self.path = document_path
        self.full_name = os.path.basename(self.path)
        if os.path.isdir(document_path):
            self.file_type = 'dir'
            print('dir')
        elif os.path.isfile(document_path):
            self.file_type = 'file'
            print('file')
        else:
            raise Exception

    def move_to_dir(self, new_path, overwrite=False):
        # check if document exists at new path
        if os.path.exists(new_path + self.full_name):
            if overwrite:
                # move old file/directory to trash can
                # we always don't want accidentally removing
                send2trash.send2trash(new_path + self.full_name)
            else:
                raise PathAlreadyExistException
        # shutil.move can't handle alias file in MacOS!!
        if platform.system() == 'Darwin':
            status = subprocess.call('mv ' + self.path + ' ' + new_path, shell=True)
            if status != 0:
                raise IOError
        else:
            shutil.move(self.path, new_path)
        self.path = new_path + self.full_name


if __name__ == '__main__':
    pass


