import re

from . import constraints


class ValidationError(Exception):
    '''
    Raised whenever a validator in this module determines the value passed
    to .validate() fails validation.
    '''
    pass


class ValidatorBase(object):
    '''
    This should be the absolute base class for all validators.
    It doesn't nothing special, but allows derrived classes to call .validate()
    on super() with reckless abandon!
    '''
    def __init__(self, *args, **kwargs):
        pass

    def validate(self, value):
        '''
        Given a value, raises a ValueError if validation fails, otherwise
        returns None.
        :param value: The object to test for Validation.
        '''


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
    minimum and maximum length.  If no minimum length is given,
    the string may be None.
    '''
    def __init__(self, min_length=None, max_length=None, *args, **kwargs):
        '''
        Creates a new instance of LengthValidator.

        :param min_length: Minimum required length for a string.
        :param max_length: Maximum allowed length for a string.
        '''

        if None not in [min_length, max_length]:
            if max_length < min_length:
                raise ValueError()

        self.min_length = min_length
        self.max_length = max_length

        super(LengthValidator, self).__init__(**kwargs)

    def validate(self, value):

        if self.max_length:
            if value and len(value) > self.max_length:
                raise ValidationError(
                    "{value} longer than max_length"
                    "{max_length}".format(value=value,
                                          max_length=self.max_length))

        if self.min_length:
            if value is None:
                raise ValidationError(
                    "{value} shorter than min_length"
                    "{min_length}".format(value=value,
                                          min_length=self.min_length))

            if len(value) < self.min_length:
                raise ValidationError(
                    "{value} shorter than min_length"
                    "{min_length}".format(value=value,
                                          min_length=self.min_length))

        super(LengthValidator, self).validate(value)


class RegexValidator(ValidatorBase):
    '''
    Tests a given string value against a regular expression.
    The test is skipped if validate() receives a value of None
    '''
    def __init__(self, pattern, *args, **kwargs):
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
    pass


class NumericValidator(RequiredValidator, ValidatorBase):
    '''
    Tests that the provided value is a python numeric type.
    '''
    def validate(self, value):
        if value is not None:
            if type(value) not in [int, float, long]:
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
        super(AddressValidator, self).__init__(max_length=200,
                                               *args,
                                               **kwargs)


class PostalcodeValidator(RequiredValidator, RegexValidator):
    '''
    Tests that a string is a valid length and format for a
    Postal Code.  It can be a maximum of 10 digits and may
    also contain spaces and hyphens (-).
    '''
    def __init__(self, *args, **kwargs):
        super(PostalcodeValidator, self).__init__(
            pattern=r'^([\d -]{1,10})$',
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


class PhoneValidator(RequiredValidator, RegexValidator):
    '''
    Tests that a string looks like a phone number (between 5 and 19 characters)
    and only contains the characters 0-9, +, -, (, and ).
    '''
    def __init__(self, *args, **kwargs):
        # todo: this regex is flawed.. + needs to match at the front only
        # only while still providing validation
        super(PhoneValidator, self).__init__(
            pattern=r'^([\+\d\-\(\) ]){5,19}$',
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
            # pattern=r'(\w+[.|\w])+@(\w+[.])*\w+', -- no good
            pattern=r'.*',
            max_length=constraints.MAX_EMAIL_LENGTH,
            *args,
            **kwargs)


class CountrycodeValidator(RequiredValidator, LengthValidator):
    def __init__(self, *args, **kwargs):
        super(CountrycodeValidator, self).__init__(
            max_length=constraints.MAX_COUNTRYCODE_LENGTH,
            *args,
            **kwargs)


class PassthroughValidator(RequiredValidator):
    '''
    Allows validation of a subentity type that implements validators
    on it's own properties.  See request.ChargeRequest() for more
    information
    '''
    def validate(self, value):
        if value is not None:
            value.validate_all()
        super(PassthroughValidator, self).validate(value)


# TODO: it would be cool to replace this with a pass-through validator instead
class DummyValidator(ValidatorBase):
    '''
    This is a special case validator that never fails validation and accepts
    and parameters passed to it's constructor.  Useful for attributes that
    don't contain basic types (), but instead provide their own validation.
    '''
    pass
