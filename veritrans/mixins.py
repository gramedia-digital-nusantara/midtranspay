import re


class ValidatableMixin(object):

    def validate_attr(self, name, value, pattern):
        if not re.match(pattern, value, re.DOTALL):
            raise ValueError(
                "{attr_name} did not pass validation. ("
                "Expression: {validation_expr} | "
                "Value: {attr_value})".format(
                    attr_name=name,
                    validation_expr=pattern,
                    attr_value=value))

    def validate_all(self):
        ''' Validates all of the current instance's properties.
        If one of the instances does not validate, then a ValueError
        will be thrown on the first failure.
        '''
        for attr_name in self._validators:
            # in the event of None, we're switching to "" to validate
            value = getattr(attr_name) or ''
            validator = self._validators[attr_name]
            self.validate_attr('attr_name', value, validator)


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
