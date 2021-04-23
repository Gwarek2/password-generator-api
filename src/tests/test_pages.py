import unittest

from src.application import app


class ApplicationTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
