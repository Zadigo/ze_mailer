import csv
import os

from ze_mailer.app.core.errors import FileTypeError
from ze_mailer.app.core.messages import Info
from ze_mailer.app.core.mixins.utilities import UtilitiesMixin

# from ze_mailer.app.core.settings import configuration


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
