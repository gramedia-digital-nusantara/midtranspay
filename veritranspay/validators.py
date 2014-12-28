'''
A simple set of validation classes that are used to check entities in
:py:mod:`veritranspay.request`, to give us some assurance they have
provided the required data, in the required format, for Veritrans to
accept the request.

(Although Veritrans will validate this data as well, this is done so we
don't waste time submitting data we can already know will be rejected).

When any of the Validators defined in this module fail, they raise a
:py:class:`veritranspay.validators.ValidationError`.

See the following for more details:

- http://docs.veritrans.co.id/sandbox/other_commands.html
- http://docs.veritrans.co.id/sandbox/charge.html
'''
from numbers import Number
import re

from . import constraints


class ValidationError(Exception):
    '''
    Raised whenever a validator in this module determines the value passed
    to .validate() fails validation.
    '''
    def __init__(self, message=None):
        self.message = message


class ValidatorBase(object):
    '''
    This should be the absolute base class for all validators.
    It doesn't nothing special, but allows derrived classes to call .validate()
    on super() with reckless abandon!
    '''
    def __init__(self, *args, **kwargs):
        return

    def validate(self, value):
        '''
        Given a value, raises a ValueError if validation fails, otherwise
        returns None.

        :param value: The object to test for Validation.
        '''
        return


class DummyValidator(ValidatorBase):
    '''
    This is a special case validator that never fails validation and accepts
    and parameters passed to it's constructor.
    '''
    pass


class RequiredValidator(ValidatorBase):
    '''
    Asserts that a value is not null when it's is_required attribute
    is set to 'True'
    '''
    def __init__(self, is_required=True, *args, **kwargs):
        '''
        Creates a new instance of RequiredValidator.

        :param is_required: When True (or not provided), validate()
            will fail on None values.
        :type is_required: :py:class:`bool`
        '''
        self.is_required = is_required
        super(RequiredValidator, self).__init__(**kwargs)

    def validate(self, value):
        if self.is_required and value is None:
            raise ValidationError("Required value was None")
        super(RequiredValidator, self).validate(value)


class LengthValidator(ValidatorBase):
    '''
    Asserts that a string's length is between a given
    minimum and/or maximum length.
    '''
    def __init__(self, min_length=None, max_length=None, *args, **kwargs):
        '''
        Creates a new instance of LengthValidator.

        :param min_length: Minimum required length for a string.
        :type min_length: :py:class:`int`
        :param max_length: Maximum allowed length for a string.
        :type min_length: :py:class:`int`
        '''
        if None not in [min_length, max_length]:
            if max_length < min_length:
                raise ValueError()

        self.min_length = min_length
        self.max_length = max_length

        super(LengthValidator, self).__init__(**kwargs)

    def validate(self, value):

        if self.max_length and value is not None:
            if value and len(value) > self.max_length:
                raise ValidationError(
                    "{value} longer than max_length "
                    "{max_length}".format(value=value,
                                          max_length=self.max_length))

        if self.min_length and value is not None:
            if len(value) < self.min_length:
                raise ValidationError(
                    "{value} shorter than min_length "
                    "{min_length}".format(value=value,
                                          min_length=self.min_length))

        super(LengthValidator, self).validate(value)


class RegexValidator(ValidatorBase):
    '''
    Tests a given string value against a regular expression.
    '''
    def __init__(self, pattern, *args, **kwargs):
        '''
        :param pattern: A regular expression pattern.
        :type pattern: :py:class:`str`
        '''
        self.pattern = pattern
        super(RegexValidator, self).__init__(**kwargs)

    def validate(self, value):
        # regex validator should skip its tests when value is None
        if value is not None:
            if not re.match(self.pattern, value, re.DOTALL):
                raise ValidationError(
                    "{value} did not match expected pattern"
                    "{pattern}".format(value=value,
                                       pattern=self.pattern))

        super(RegexValidator, self).validate(value)


class StringValidator(RequiredValidator, LengthValidator):
    '''
    Takes a string value.  Can optionally required the string to not be
    null by setting is_required to True (it's default),
    greater-than-or-equal to a min_length or
    less-than-or-equal-to a max_length.
    '''
    def validate(self, value):
        if value is not None:

            # python 3 removes basestring
            try:
                string_type = basestring
                # v -- this doesn't work?  works in python but not in nosetests
                # string_type = getattr(__builtins__, 'basestring', str)
            except NameError:
                string_type = str

            if not isinstance(value, string_type):
                raise ValidationError(
                    "{value} ({type}) is not "
                    "a string".format(value=value, type=type(value)))
        super(StringValidator, self).validate(value)


class NumericValidator(RequiredValidator):
    '''
    Tests that the provided value is a python numeric type.
    '''
    def validate(self, value):
        if value is not None:
            if not isinstance(value, Number):
                raise ValidationError("{value} ({type}) is not numeric".format(
                    value=value,
                    type=type(value)))
        super(NumericValidator, self).validate(value)


class AddressValidator(RequiredValidator, LengthValidator):
    '''
    Tests that a provided string is a valid length for address.
    If not required is_required should be set to false in the
    constructor.
    '''
    def __init__(self, *args, **kwargs):
        super(AddressValidator, self).__init__(
            max_length=constraints.MAX_ADDRESS_LENGTH,
            *args,
            **kwargs)


class PostalcodeValidator(RequiredValidator, RegexValidator, LengthValidator):
    '''
    Tests that a string is a valid length and format for a
    Postal Code.  It can be a maximum of 10 digits and may
    also contain spaces and hyphens (-).
    '''
    def __init__(self, *args, **kwargs):
        super(PostalcodeValidator, self).__init__(
            pattern=r'^([\d -])*$',
            max_length=constraints.MAX_POSTALCODE_LENGTH,
            *args,
            **kwargs)


class NameValidator(RequiredValidator, LengthValidator):
    '''
    Tests that a human name (eg, given or sirname) are at most 20
    characters in length.
    '''
    def __init__(self, *args, **kwargs):
        super(NameValidator, self).__init__(
            max_length=constraints.MAX_NAME_LENGTH,
            *args,
            **kwargs)


class CityValidator(NameValidator):
    '''
    Acts as an Alias for NameValidator, since their defined validation
    behavior is the same.
    '''
    pass


class PhoneValidator(RequiredValidator, RegexValidator, LengthValidator):
    '''
    Tests that a string looks like a phone number (between 5 and 19 characters)
    and only contains the characters 0-9, +, -, (, and ).
    '''
    def __init__(self, *args, **kwargs):
        super(PhoneValidator, self).__init__(
            pattern=r'^\+?[\d\-\(\) ]*$',
            min_length=constraints.MIN_PHONE_LENGTH,
            max_length=constraints.MAX_PHONE_LENGTH,
            *args,
            **kwargs)


class EmailValidator(RequiredValidator, RegexValidator, LengthValidator):
    '''
    Tests that a given string is less than 45 characters in length and
    vaguely appears to be in the proper format for an e-mail address.
    '''
    # NOTE: this is actually a REALLY complicated problem
    # http://ex-parrot.com/~pdw/Mail-RFC822-Address.html
    # the goal here is just a simple 'does it kinda look like an email'
    def __init__(self, *args, **kwargs):
        super(EmailValidator, self).__init__(
            pattern=r'^.+@.+$',
            max_length=constraints.MAX_EMAIL_LENGTH,
            *args,
            **kwargs)


class CountrycodeValidator(RequiredValidator, LengthValidator):
    '''
    Validates that a country code is in a format that Veritrans
    accepts -- which is any string less than 10 characters (note:
    their API documentation states this should be ISO 3166-1 Alpha 3)
    '''
    def __init__(self, *args, **kwargs):
        super(CountrycodeValidator, self).__init__(
            max_length=constraints.MAX_COUNTRYCODE_LENGTH,
            *args,
            **kwargs)


class PassthroughValidator(RequiredValidator):
    '''
    Allows validation of a subentity type that implements validators
    on it's own properties.  See request.ChargeRequest() for more
    information.
    If Value is an iterable, validate_all() will be called on each of
    it's elements.
    '''
    def validate(self, value):
        if value is not None:
            try:
                for child in iter(value):
                    child.validate_all()
            except TypeError:
                value.validate_all()

        super(PassthroughValidator, self).validate(value)
