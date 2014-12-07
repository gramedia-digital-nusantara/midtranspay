import unittest

from faker import Faker

from veritranspay import validators

fake = Faker()


class RequiredValidator_UnitTests(unittest.TestCase):
    '''
    Checks validators.RequiredValidator's behavior.
    '''

    def test_is_required_default_true(self):
        '''
        When the is_required init param is not provided, it's expected
        default is True
        '''
        v = validators.RequiredValidator()
        self.assertTrue(v.is_required)

    def test_validate_None_raises_ValidationError(self):
        '''
        When is_required == True, a ValidationError should be raised if
        None is passed to .validate()
        '''
        v = validators.RequiredValidator()
        self.assertRaises(validators.ValidationError,
                          lambda: v.validate(None))

    def test_always_validates_if_is_required_eq_False(self):
        '''
        When is_required == False, validate() should succeed when passed None.
        '''
        v = validators.RequiredValidator(is_required=False)
        v.validate(None)

    def test_non_None_values_always_pass(self):
        '''
        Values that are not None should always pass validation, regardless
        of whether is_required is True or false.
        '''
        v_req = validators.RequiredValidator()
        v_opt = validators.RequiredValidator(is_required=False)

        # the first few values are things that will boolean evaluate false
        # just to make sure we aren't doing the wrong thing in validation
        test_values = ([],
                       False,
                       '',
                       fake.text(),
                       fake.pydict(),
                       )

        for value in test_values:
            v_req.validate(value)
            v_opt.validate(value)

    def test_validate_returns_None(self):
        '''
        When validate() passes, it should return None.
        '''
        v = validators.RequiredValidator()
        result = v.validate(fake.pystr())
        self.assertIsNone(result)


class LengthValidator_UnitTests(unittest.TestCase):

    def test_invalid_init_args_raise_ValueError(self):
        ''' max_length cannot be less than min_length on init. '''
        self.assertRaises(ValueError,
                          lambda: validators.LengthValidator(min_length=10,
                                                             max_length=5))

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


class RegexValidator_UnitTests(unittest.TestCase):

    def test_pattern_matching(self):
        ''' Verify that regex pattern validation is occurring. '''
        test_digit_pattern = r'^\d+$'

        v = validators.RegexValidator(pattern=test_digit_pattern)

        bad_value = ''.join([fake.random_letter() for _ in range(10)])
        good_value = ''.join([str(fake.random_digit()) for _ in range(10)])

        l = lambda: v.validate(bad_value)
        self.assertRaises(validators.ValidationError, l)

        self.assertIsNone(v.validate(good_value))


class NumericValidator_UnitTests(unittest.TestCase):

    def test_numbers_accepted(self):

        v = validators.NumericValidator()

        good_float = fake.pyfloat()
        good_int = fake.pyint()
        good_long = long(good_int)

        for good in [good_float, good_int, good_long]:
            result = v.validate(good)
            self.assertIsNone(result)

    def test_letters_rejected(self):

        v = validators.NumericValidator()

        bad_stringified_int = str(fake.pyint())
        bad_letters = fake.word()

        for bad in [bad_stringified_int, bad_letters]:
            l = lambda: v.validate(bad)
            self.assertRaises(validators.ValidationError, l)


class StringValidator_UnitTests(unittest.TestCase):

    def test(self):
        self.skipTest("Implement me!")