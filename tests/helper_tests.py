import unittest
from datetime import datetime

from veritranspay import helpers


class ParseDatetimeHelper_UnitTests(unittest.TestCase):

    def test_parse_datetime_returns_expected(self):
        '''
        Make sure our datetime parsing returns a date that we're expecting.
        '''
        val = "2014-08-24 15:39:22"
        expected = datetime(2014, 8, 24, 15, 39, 22)
        actual = helpers.parse_veritrans_datetime(val)
        self.assertEqual(actual, expected)

    def test_returned_datetime_is_naive(self):
        '''
        Returns datetimes should be naive (not timezone aware).
        '''
        val = "2014-08-24 15:39:22"
        actual = helpers.parse_veritrans_datetime(val)

        self.assertIsNone(actual.tzinfo)


class ParseCurrencyHelper_UnitTests(unittest.TestCase):

    def test_returns_integer(self):
        val = "100.00"
        actual = helpers.parse_veritrans_amount(val)
        self.assertIsInstance(actual, int)

    def test_ignores_fractional(self):
        val = "100.99"
        expected = 100
        actual = helpers.parse_veritrans_amount(val)
        self.assertEqual(actual, expected)

    def test_none_input_returns_0(self):
        val = None
        expected = 0
        actual = helpers.parse_veritrans_amount(val)
        self.assertEqual(actual, expected)

    def test_emptystring_input_returns_0(self):
        val = ''
        expected = 0
        actual = helpers.parse_veritrans_amount(val)
        self.assertEqual(actual, expected)
