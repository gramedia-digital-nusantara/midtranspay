from . import validators


class ValidatableMixin(object):

    def validate_attr(self, name, value, validator):
        try:
            validator.validate(value)
        except validators.ValidationError as e:
            msg = "{name} failed validation: {message}".format(
                name=name,
                message=e.message)
            raise validators.ValidationError(msg)

    def validate_all(self):
        for attr_name in self._validators:
            value = getattr(self, attr_name)
            validator = self._validators[attr_name]
            self.validate_attr(attr_name, value, validator)


class SerializableMixin(object):

    def serialize(self):
        return self.__dict__


class RequestEntity(ValidatableMixin, SerializableMixin):

    def serialize(self):
        ''' Serializes the object, but first validates all
        the attributes of this class.
        '''
        self.validate_all()
        return SerializableMixin.serialize(self)
