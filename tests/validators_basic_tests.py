'''
Validation logic tests for our simple validators.
These generally serve as building block for more complex validator
types (but not always.  In some cases they're used directly).

All the validators live together in the veritranspay.validators module.
'''
from random import randint
import unittest

from faker import Faker

from veritranspay import validators


fake = Faker()


class ValidatorBase_UnitTests(unittest.TestCase):
    ''' Unit tests for veritranspay.validators.ValidatorBase. '''
    def test_init_accepts_any_args(self):
        '''
        Init should accept any or no keyword or positionl arguments provided
        to it.
        '''
        # generate a random amount of fake text/numeric array elements
        args = fake.words(fake.random_digit()) + \
            [fake.random_number() for _ in range(randint(5, 10))]

        validators.ValidatorBase(*args)

        # generate a fake dictionary to use as keyword args
        kwargs = fake.pydict(randint(5, 10))

        validators.ValidatorBase(**kwargs)

        # make sure it accepts no args
        validators.ValidatorBase()

        # if no exceptions thrown, then this test passes.
        self.assertTrue(True)

    def test_validate_accepts_any_single_arg(self):
        '''
        Calls to validate accept a single argument,
        including None and always return None on successful call.
        '''
        v = validators.ValidatorBase()

        # must take at least 1 arg
        self.assertRaises(TypeError, lambda: v.validate())

        # cannot take two args
        args = fake.words(2)
        self.assertRaises(TypeError, lambda: v.validate(*args))

        # successful call should return nothing
        return_val = v.validate(value=fake.word())
        self.assertIsNone(return_val)

        return_val = v.validate(None)
        self.assertIsNone(return_val)


class DummyValidator_UnitTests(ValidatorBase_UnitTests):
    ''' Unit tests for veritranspay.validators.DummyValidator. '''
    pass


class RequiredValidator_UnitTests(unittest.TestCase):
    ''' Unit tests for veritranspay.validators.RequiredValidator. '''
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
    ''' Unit tests for veritranspay.validators.LengthValidator '''

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

        bad_empty = ''
        bad_too_short = ''.join([fake.random_letter() for _ in range(3)])

        for bad in [bad_empty, bad_too_short]:
            l = lambda: v.validate(bad)
            self.assertRaises(validators.ValidationError, l)

    def test_min_max_enforced(self):
        '''
        min_value and max_value should both apply if both are
        provided to the constructor.
        '''
        v = validators.LengthValidator(min_length=5, max_length=5)

        good_len = ''.join([fake.random_letter() for _ in range(5)])

        for good in [good_len]:
            self.assertIsNone(v.validate(good))

        bad_too_short = ''.join([fake.random_letter() for _ in range(4)])
        bad_too_long = ''.join([fake.random_letter() for _ in range(6)])

        for bad in [bad_too_short, bad_too_long]:
            l = lambda: v.validate(bad)
            self.assertRaises(validators.ValidationError, l)


class RegexValidator_UnitTests(unittest.TestCase):
    ''' Unit tests for veritranspay.validators.RegexValidator '''
    def test_pattern_matching(self):
        ''' Verify that regex pattern validation is occurring. '''
        test_digit_pattern = r'^\d+$'

        v = validators.RegexValidator(pattern=test_digit_pattern)

        bad_value = ''.join([fake.random_letter() for _ in range(10)])
        good_value = ''.join([str(fake.random_digit()) for _ in range(10)])

        l = lambda: v.validate(bad_value)
        self.assertRaises(validators.ValidationError, l)

        self.assertIsNone(v.validate(good_value))


class StringValidator_UnitTests(unittest.TestCase):
    ''' Unit tests for veritranspay.validators.StringValidator '''
    def test_strings_accepted(self):
        ''' Any string value should be accepted '''
        v = validators.StringValidator()
        for val in fake.words(randint(5, 10)) + fake.sentences(randint(5, 10)):
            return_val = v.validate(val)
            self.assertIsNone(return_val)

    def test_numbers_rejected(self):
        ''' Numeric values should raise a validation error '''
        v = validators.StringValidator()
        self.assertRaises(validators.ValidationError,
                          lambda: v.validate(fake.random_number()))


class NumericValidator_UnitTests(unittest.TestCase):
    ''' Unit tests for veritranspay.validators.NumericValidator '''
    def test_numbers_accepted(self):
        ''' floats, ints, and longs should all pass validation. '''
        v = validators.NumericValidator()

        good_float = fake.pyfloat()
        good_int = fake.pyint()

        # python 3 removes long (ints are longs)
        if hasattr(__builtins__, 'long'):
            good_long = long(good_int)
        else:
            good_long = fake.pyint()

        for good in [good_float, good_int, good_long]:
            result = v.validate(good)
            self.assertIsNone(result)

    def test_letters_rejected(self):
        ''' string/unicode values should raise a ValidationError. '''
        v = validators.NumericValidator()

        bad_stringified_int = str(fake.pyint())
        bad_letters = fake.word()

        for bad in [bad_stringified_int, bad_letters]:
            l = lambda: v.validate(bad)
            self.assertRaises(validators.ValidationError, l)
