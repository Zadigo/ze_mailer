import unittest

from ze_mailer.app.core.config.settings import Configuration, configuration


class TestConfiguration(unittest.TestCase):
    def setUp(self):
        self.settings = configuration

    def test_is_dict(self):
        self.assertIsInstance(self.settings, dict)

    def test_base_values(self):
        self.assertIn('base_dir', self.settings)
        self.assertIn('data_dir', self.settings)

    def test_added_value_in_dict(self):
        self.settings['custom_value'] = 'value'
        self.assertIn('custom_value', self.settings)
        self.assertEqual(self.settings['custom_value'], 'value')

if __name__ == "__main__":
    unittest.main()
