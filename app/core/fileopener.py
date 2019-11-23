import csv
import os
# from ze_mailer.app.core.settings import configuration
from collections import OrderedDict
from pathlib import Path

from ze_mailer.app.core.errors import FileTypeError
from ze_mailer.app.core.messages import Info
from ze_mailer.app.core.mixins.utilities import UtilitiesMixin


class FilesObject:
    """A dictionnary object that holds files in a directory and
    facilitates actions such as getting them back with ease
    """
    files = OrderedDict()

    def __getitem__(self, key):
        try:
            item = self.files[key]
        except FileExistsError:
            raise
        return item

    def __getattribute__(self, name):
        if name == 'files' and len(self.files) == 0:
            return []
        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name == 'files':
            if not isinstance(value, (dict, OrderedDict)):
                raise TypeError('The files attribute should be a dictionnary object'
                        ' e.g. dict, OrderedDict')
        return super().__setattr__(name, value)

    def append(self, file_directory, filename):
        """Appends an item to files
        """
        name, extension = filename.split('.')

        full_path = os.path.join(file_directory, filename)
        file_item = {
            name: {
                'extension': extension,
                'path': full_path,
                'object': Path(full_path)
            }
        }
        self.files.update(file_item)

    @classmethod
    def get_object(cls, key):
        """Gets a file and returns the Path() element
        """
        selected_file = cls.__getitem__(key)
        return selected_file['object']

    @classmethod
    def scan_directory(cls, directory_path, exclude_files: list=None, *args):
        """Scans the data directory in order to get
        all the files within it and return and the object
        elements

        Description
        -----------
            Wraps the file in the FilesObject which returns
            the following dictionnary for a selected file:

                {
                    name: {
                        extension: extension,
                        path: full_path,
                        object: Path(full_path)
                    }
                }
        """
        # If there are no files in the directory or there
        # someking of mishap where the wrong directory is
        # selected for example, return empy generator
        filenames = list(os.walk(directory_path))
        if len(filenames) == 0:
            return cls

        for filename in filenames:
            if filename not in exclude_files:
                cls.append(directory_path, filename)
        return cls

class FileOpener(UtilitiesMixin):
    def __init__(self, file_path=None):
        if not file_path.endswith('csv'):
            message = 'Your file should be a csv file'
            raise FileTypeError(message, file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            csv_file = csv.reader(f)
            csv_content = list(csv_file).copy()

        # Pop the headers but keep
        # them for later usage
        self.headers = csv_content.pop(0)

        # Clean and normalize all the names
        # and store the csv's content
        self.csv_content = self.normalize_names(csv_content)

    def print_to_file(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            # Recompose the header and the content
            data = self.csv_content.prepend(self.headers)
            csv_file = csv.writer(f)
            for row in data:
                csv_file.writerow(row)
        return Info('Wrote %s names to %s' % (len(self.csv_content), os.path.basename(file_path)))
# FileOpener(file_path=configuration['dummy_file'])
