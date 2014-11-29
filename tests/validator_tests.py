import unittest

from faker import Faker

from veritrans import new_validators as validators


fake = Faker()


class ValidatorTestsBase(object):
    pass


class LengthValidator_UnitTests(unittest.TestCase):

    def test_invalid_init_args(self):
        ''' max_length cannot be less than min_length on init. '''
        l = lambda: validators.LengthValidator(min_length=10, max_length=5)
        self.assertRaises(ValueError, l)

    def test_max_enforced(self):
        ''' max_length is enforced when no min_length is provided. '''
        v = validators.LengthValidator(max_length=10)

        good_empty = ''
        good_none = None
        good_len = ''.join([fake.random_letter() for _ in range(5)])
        good_max_len = ''.join([fake.random_letter() for _ in range(10)])

        for good in [good_empty, good_none, good_len, good_max_len]:
            self.assertIsNone(v.validate(good))

        bad_too_long = ''.join([fake.random_letter() for _ in range(11)])
        for bad in [bad_too_long]:
            l = lambda: v.validate(bad)
            self.assertRaises(validators.ValidationError, l)

    def test_min_enforced(self):
        ''' min_legnth is enforced, when no max_legnth is provided. '''

        v = validators.LengthValidator(min_length=5)

        good_len = ''.join([fake.random_letter() for _ in range(5)])

        for good in [good_len]:
            self.assertIsNone(v.validate(good))

        bad_none = None
        bad_empty = ''
        bad_too_short = ''.join([fake.random_letter() for _ in range(3)])

        for bad in [bad_none, bad_empty, bad_too_short]:
            l = lambda: v.validate(bad)
            self.assertRaises(validators.ValidationError, l)

    def test_min_max_enforced(self):
        ''' min_value and max_value should both apply if both are
        provided to the constructor.
        '''

        v = validators.LengthValidator(min_length=5, max_length=5)

        good_len = ''.join([fake.random_letter() for _ in range(5)])

        for good in [good_len]:
            self.assertIsNone(v.validate(good))

        bad_none = None
        bad_too_short = ''.join([fake.random_letter() for _ in range(4)])
        bad_too_long = ''.join([fake.random_letter() for _ in range(6)])

        for bad in [bad_none, bad_too_short, bad_too_long]:
            l = lambda: v.validate(bad)
            self.assertRaises(validators.ValidationError, l)
