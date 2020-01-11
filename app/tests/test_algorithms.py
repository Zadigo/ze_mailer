import unittest
from ze_mailer.app.patterns.algorithms import SimpleNamesAlgorithm

class TestSimpleAlgorithm(unittest.TestCase):
    def setUp(self):
        self.simple_algorithm = SimpleNamesAlgorithm('Eugenie Bouchard')

    def test_is_array(self):
        self.assertIsInstance(self.simple_algorithm.patterns, list)

    def test_one_sample_value(self):
        self.assertIn('eugenie.bouchard@gmail.com', self.simple_algorithm.patterns)
        self.assertIn('eugenie-bouchard@gmail.com', self.simple_algorithm.patterns)

    def test_can_get_item(self):
        # Tests whether we can do a subscription
        # in the same manner we can do with a list
        self.assertEqual('eugenie.bouchard@gmail.com', self.simple_algorithm[0])

    def test_iteration(self):
        # Test that we can iterate over the
        # different values
        for item in self.simple_algorithm:
            last_item = item

        self.assertIsNotNone(last_item)
        self.assertEqual(last_item, 'eugenie_bouchard@outlook.com')

    def test_can_append(self):
        values = self.simple_algorithm.append('eugenie.bouchard@google.fr')
        self.assertIsInstance(values, list)
        self.assertIsInstance(self.simple_algorithm.patterns, list)
        self.assertIn('eugenie.bouchard@google.fr', self.simple_algorithm)

if __name__ == "__main__":
    unittest.main()