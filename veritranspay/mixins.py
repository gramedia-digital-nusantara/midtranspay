from . import validators


class ValidatableMixin(object):
    '''
    Provides a mechanism for validating the attributes of an object instance.
    Expects a dictionary named _validators to be provided with keys that
    represent the names of attributes to be validated, mapped to an instance
    of a class in the module :py:mod:`veritranspay.validators`.
    '''
    def validate_attr(self, name, value, validator):
        '''
        Tries to validate the provided value with a given validator.
        If validation fails, a ValidationError will be raised indicating
        the name of the property the failed, along with the error message.

        :arg name: Name of the attribute being validated. This is only used
            for the error message when validation fails.
        :type name: :py:class:`str`
        :arg value: The value that will actually be validated.
        :arg validator: The appropriate validator instance that
            value will be checked with.
        :type validator: Subclass of
            :py:class:`veritranspay.validators.ValidatorBase`
        :raises: :py:class:`veritranspay.validators.ValidationError`
        '''
        try:
            validator.validate(value)
        except validators.ValidationError as e:
            msg = "{name} failed validation: {message}".format(
                name=name,
                message=e.message)
            raise validators.ValidationError(msg)

    def validate_all(self):
        '''
        Iterates over all the validators in this instances _validators
        dictionary, and validates a matching attribute on this object
        with a validator listed in the _validators dictionary.
        '''
        for attr_name in self._validators:
            value = getattr(self, attr_name)
            validator = self._validators[attr_name]
            self.validate_attr(attr_name, value, validator)


class SerializableMixin(object):
    '''
    An instance that can return a dictionary representation of it's
    properties by calling a serialize() method.
    '''
    def serialize(self):
        '''
        Returns a dictionary representing the current object.  If attributes
        of the current object also implement a serialize method, their
        dictionary representation will be added as well, instead of the object
        itself.
        :returns: Dictionary representation of an object.
        :rtype: :py:class:`dict`
        '''
        rv = {}
        for key in self.__dict__:
            val = getattr(self, key)

            # If a given attribute implements a 'serialize' method, call
            # that instead of just adding the attribute to the dictionary.
            if hasattr(val, 'serialize'):
                rv[key] = val.serialize()
            else:
                rv[key] = val

        return rv


class RequestEntity(ValidatableMixin, SerializableMixin):
    '''
    Provides no functionality, other than incorporating SerializableMixin
    and ValiditableMixin in a single base class.
    '''
    def __repr__(self):
        return '<{klass}()>'.format(klass=self.__class__.__name__)
