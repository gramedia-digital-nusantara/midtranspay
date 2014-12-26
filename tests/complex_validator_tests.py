'''
Validation tests for our 'complex' validators.
These are all built on top of our basic validator types and stand
to validate a specific type of data as defined by the Veritrans v2 API.

All the validators live together in the veritranspay.validators module.
'''
from random import randint
import unittest

from faker import Faker
from mock import MagicMock

from veritranspay import validators


fake = Faker()


class BaseTest_RequiredValidator(object):
    '''
    Mixin for any testing any validators that implement specifying
    is_required as an init param.
    Derrived classes must specify a VALIDATOR_CLASS attribute on their class.
    '''
    def test_required_by_default(self):
        ''' None should raise ValidationError by default '''
        v = self.VALIDATOR_CLASS()
        l = lambda: v.validate(None)
        self.assertRaises(validators.ValidationError, l)

    def test_None_passes_when_is_required_False(self):
        ''' A value of None can pass, if is_required=False specified to init '''
        v = self.VALIDATOR_CLASS(is_required=False)
        result = v.validate(None)
        self.assertIsNone(result)


class AddressVaildator_UnitTests(BaseTest_RequiredValidator,
                                 unittest.TestCase):
    '''
    Unit tests for veritranspay.validators.AddressValidator.
    '''
    VALIDATOR_CLASS = validators.AddressValidator

    def test_maximum_200_chars(self):
        ''' Values longer than 200 chars should raise a ValidationError. '''
        v = validators.AddressValidator()
        long_val = "".join([fake.random_letter() for _ in range(201)])
        self.assertRaises(validators.ValidationError,
                          lambda: v.validate(long_val))

    def test_good_address_validates(self):
        ''' Addresses 200 chars or less should pass validation. '''
        v = validators.AddressValidator()
        good_val = "".join([fake.random_letter() for _ in range(200)])
        return_val = v.validate(good_val)
        self.assertIsNone(return_val)


class PostalCodeValidator_UnitTests(BaseTest_RequiredValidator,
                                    unittest.TestCase):
    '''
    Unit tests for veritranspay.validators.PostalcodeValidator
    '''
    VALIDATOR_CLASS = validators.PostalcodeValidator

    def test_maximum_10_characters(self):
        ''' Postal codes longer than 10 chars should raise a ValidationError'''
        v = validators.PostalcodeValidator()
        long_pc = ''.join([str(fake.random_digit()) for _ in range(11)])
        l = lambda: v.validate(long_pc)
        self.assertRaises(validators.ValidationError, l)

    def test_good_postalcodes_validate(self):
        ''' Generates 100 random postal codes and validates them. '''
        v = validators.PostalcodeValidator()
        for pc in [fake.postcode() for _ in range(100)]:
            result = v.validate(pc)
            self.assertIsNone(result)


class NameValidator_UnitTests(BaseTest_RequiredValidator,
                              unittest.TestCase):
    '''
    Unit tests for veritranspay.validators.NameValidator
    '''
    VALIDATOR_CLASS = validators.NameValidator

    def test_maximum_20_characters(self):
        ''' Names longer than 20 chars should raise ValidationError. '''
        v = validators.NameValidator()
        long_name = ''.join([fake.random_letter() for _ in range(21)])
        l = lambda: v.validate(long_name)
        self.assertRaises(validators.ValidationError, l)

    def test_good_names_validate(self):
        ''' Valid names should pass validation. '''
        v = validators.NameValidator()
        for _ in range(10):
            name = ''.join([fake.random_letter()
                            for _ in range(randint(1, 20))])
            result = v.validate(name)
            self.assertIsNone(result)


class CityValidator_UnitTests(BaseTest_RequiredValidator,
                              unittest.TestCase):
    '''
    Unit tests for veritranspay.validators.CityValidator
    '''
    VALIDATOR_CLASS = validators.CityValidator

    def test_maximum_20_characters(self):
        ''' Cities longer than 20 chars should raise a ValidationError. '''
        v = validators.CityValidator()
        long_city = ''.join([fake.random_letter() for _ in range(21)])
        l = lambda: v.validate(long_city)
        self.assertRaises(validators.ValidationError, l)

    def test_valid_cities_pass_validation(self):
        ''' Valid city names should pass validation '''
        v = validators.CityValidator()
        for _ in range(10):
            city = ''.join([fake.random_letter()
                            for _ in range(randint(1, 20))])
            result = v.validate(city)
            self.assertIsNone(result)


class PhoneValidator_UnitTests(BaseTest_RequiredValidator,
                               unittest.TestCase):
    '''
    Unit tests for veritranspay.validators.PhoneValidator
    '''
    VALIDATOR_CLASS = validators.PhoneValidator

    def test_minimum_5_length(self):
        '''
        Phone numbers shorter than 5 chars should raise a ValidationError.
        '''
        v = validators.PhoneValidator()
        too_short = ''.join([str(fake.random_digit()) for _ in range(4)])
        l = lambda: v.validate(too_short)
        self.assertRaises(validators.ValidationError, l)

    def test_maximum_19_length(self):
        '''
        Phone numbers longer than 19 chars should raise a ValidationError.
        '''
        v = validators.PhoneValidator()
        too_long = ''.join(str(fake.random_digit()) for _ in range(20))
        l = lambda: v.validate(too_long)
        self.assertRaises(validators.ValidationError, l)

    def test_valid_phonenumbers_pass_validation(self):
        ''' Valid phone numbers should pass validation. '''
        # Note: some of the phone numbers provided by our fake library
        # won't validate here!  They contain an extension portion, which the
        # API won't accept, so we have to split them off manually.
        v = validators.PhoneValidator()
        for phonenum in [fake.phone_number().split('x')[0] for _
                         in range(100)]:
            # TODO: exclude formats with '.' by providing locale
            # for now, just skipping them manually
            if '.' in list(phonenum):
                continue
            result = v.validate(phonenum)
            self.assertIsNone(result)

    def test_invalid_phonenumbers_raise_ValidationError(self):
        '''
        Phone numbers are documented as accepting only the following
        characters: 0 through 9, +, -, space, and left+right parenthesis (,).
        Any other characters provided should raise a validation error.
        '''
        v = validators.PhoneValidator()

        # this is all the characters that we're capiable of accepting
        accepted_chars = ['+',
                          '-',
                          ' ',
                          '(',
                          ')',
                          ] + [str(dig) for dig in range(10)]

        # faker sometimes provides us with phone numbers that are too long
        # or contain an extension portion -- we want to find and USE those
        # invalid format numbers for our tests
        bad_nums = []
        for phone_num in [fake.phone_number() for _ in range(100)]:
            digs = list(phone_num)
            for d in digs:
                if d not in accepted_chars:
                    bad_nums.append(phone_num)
                    continue

        if not bad_nums:
            self.skipTest("WARNING! We didn't generate any invalid phone "
                          "numbers to test against?  You should probably "
                          "rerun these tests")
        for bad in bad_nums:
            l = lambda: v.validate(bad)
            self.assertRaises(validators.ValidationError, l)


class EmailValidator_UnitTests(BaseTest_RequiredValidator,
                               unittest.TestCase):
    '''
    Unit tests for veritranspay.validators.EmailValidator
    '''
    VALIDATOR_CLASS = validators.EmailValidator

    def test_maximum_45_length(self):
        ''' Values longer than 45 chars should raise ValidationError. '''
        v = validators.EmailValidator()
        too_long = "{0}@apps-foundry.com".format(
                       ''.join(fake.random_letter() for _ in range(50))
                    )
        l = lambda: v.validate(too_long)
        self.assertRaises(validators.ValidationError, l)

    def test_invalid_format_raise_ValidationError(self):
        ''' Invalid E-mail addresses should raise a ValidationError '''
        v = validators.EmailValidator()
        bad_email = ''.join(fake.random_letter() for _ in range(25))
        l = lambda: v.validate(bad_email)
        self.assertRaises(validators.ValidationError, l)

    def test_valid_formats_pass_validation(self):
        ''' Valid E-mail addresses should pass validation. '''
        v = validators.EmailValidator()
        for email in [fake.email() for _ in range(20)]:
            # veritrans can't accept long e-mails.. so we have to skip
            # if generated
            if len(email) > 45:
                continue
            result = v.validate(email)
            self.assertIsNone(result)


class CountrycodeValidator_UnitTests(BaseTest_RequiredValidator,
                                     unittest.TestCase):
    '''
    Unit tests for veritranspay.validators.CountrycodeValidator
    '''
    VALIDATOR_CLASS = validators.CountrycodeValidator

    def test_maximum_10_length(self):
        ''' Country codes longer than 10 chars should raise ValidationError '''
        v = validators.CountrycodeValidator()
        too_long = ''.join(fake.random_letter() for _ in range(11))
        l = lambda: v.validate(too_long)
        self.assertRaises(validators.ValidationError, l)


class PassthroughValidator_UnitTests(BaseTest_RequiredValidator,
                                     unittest.TestCase):
    '''
    Unit tests for veritranspay.validators.PassthroughValidator
    '''
    VALIDATOR_CLASS = validators.PassthroughValidator

    def test_validate_all_called_on_value(self):
        '''
        When passed a scalar, passthrough validator should call validate_all
        on the scalar.
        '''
        v = validators.PassthroughValidator()

        mock = MagicMock()
        # mocks are iterable .. we don't want that here
        mock.attach_mock(MagicMock(side_effect=TypeError), '__iter__')
        validate_mock = MagicMock()
        mock.attach_mock(validate_mock, 'validate_all')

        v.validate(mock)

        validate_mock.assert_called_once_with()

    def test_validate_all_called_on_iterable_elements(self):
        '''
        When passed an iterable, validate_all should be called on the elements
        of the iterable.
        '''
        v = validators.PassthroughValidator()

        # note: doesn't matter here whether the mocks are iterable or not
        mock1 = MagicMock()
        validate_mock1 = MagicMock()
        mock1.attach_mock(validate_mock1, 'validate_all')

        mock2 = MagicMock()
        validate_mock2 = MagicMock()
        mock2.attach_mock(validate_mock2, 'validate_all')

        mocks = [mock1, mock2]

        v.validate(mocks)

        validate_mock1.assert_called_once_with()
        validate_mock2.assert_called_once_with()
