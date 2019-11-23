import unittest

from ze_mailer.app.core.fileopener import FileOpener
from ze_mailer.app.core.settings import configuration


class TestConfiguration(unittest.TestCase):
    def setUp(self):
        self.opener = FileOpener(file_path=configuration['dummy.csv'])

    def test_is_csv(self):
        print(self.opener.csv_content)

if __name__ == "__main__":
    unittest.main()
