import unittest
import json
import sys
import os

from src.application import app


class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    # API test
    def test_no_parameters(self):
        response = self.app.get('/generate')
        self.assertEqual(response.status_code, 400)

    def test_wrong_count(self):
        parameters = ['count=24.5', 'count=abs', 'count=3',
                      'count=51', 'count=12abs', 'count=12!@#',
                      'count=9@#!abs', 'count=True', '', 'count=']
        for parameter in parameters:
            response = self.app.get(f'/generate?{parameter}&letters=on&digits=on')
            self.assertEqual(response.status_code, 400)

    def test_letters(self):
        response = self.app.get('/generate?count=12&letters=on')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        password = data.get('string')
        self.assertTrue(password.isalpha())

    def test_lower_case(self):
        response = self.app.get('/generate?count=12&lower=on')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        password = data.get('string')
        self.assertTrue(password.islower())

    def test_upper_case(self):
        response = self.app.get('/generate?count=12&upper=on')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        password = data.get('string')
        self.assertTrue(password.isupper())

    def test_custom_letters(self):
        parameter = 'abc'
        response = self.app.get(f'/generate?count=10&letters={parameter}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        password = data.get('string')
        self.assertTrue(password)
        for symbol in password:
            self.assertIn(symbol, parameter)

    def test_digits(self):
        response = self.app.get(f'/generate?count=10&digits=on')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        password = data.get('string')
        self.assertTrue(password.isalnum())

    def test_custom_digits(self):
        parameter = '123'
        response = self.app.get(f'/generate?count=10&digits={parameter}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        password = data.get('string')
        self.assertTrue(password)
        for symbol in password:
            self.assertIn(symbol, parameter)

    def test_punctuation(self):
        response = self.app.get(f'/generate?count=10&special_symbols=on')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        password = data.get('string')
        self.assertTrue(is_special_symbols(password))

    def test_custom_punctuation(self):
        parameter = '!@#$'
        response = self.app.get(f'/generate?count=10&special_symbols={parameter}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        password = data.get('string')
        self.assertTrue(password)
        for symbol in password:
            self.assertIn(symbol, parameter)

    def test_standard_password(self):
        response = self.app.get('/generate?count=10&letters=on&digits=on&special_symbols=on')
        data = json.loads(response.data)
        password = data.get('string')
        self.assertTrue(password)


if __name__ == "__main__":
    unittest.main()
