class ValidationError(Exception):
    pass


class LengthValidator(object):
    ''' Asserts that a string's length is between a given
    minimum and maximum length.  If no minimum length is given,
    the string may be None.
    '''

    def __init__(self, min_length=None, max_length=None):

        if None not in [min_length, max_length]:
            if max_length < min_length:
                raise ValueError()

        self.min_length = min_length
        self.max_length = max_length

    def validate(self, value):

        if self.max_length:
            if value and len(value) > self.max_length:
                raise ValidationError()

        if self.min_length:
            if value is None:
                raise ValidationError()

            if len(value) < self.min_length:
                raise ValidationError()
