import unittest

class PhonebookTest(unittest.TestCase):
    @unittest.skip("Skipping")
    def test_placeholder(self):
        self.assertEqual(1,2)

