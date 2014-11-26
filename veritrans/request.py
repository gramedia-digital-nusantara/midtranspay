import re


class RequestEntityBase(object):

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


class Address(RequestEntityBase):

    _validators = {'address': r'^(.{1,200})$',
                   'city': r'^(.{1,20})$',
                   'postal_code': r'^([\d -]{1,10})$',
                   'first_name': r'^(.{0,20})$',
                   'last_name': r'^(.{0,20})$',
                   'phone': r'^([\d\+\-\(\) ]{5,19})$|^$',
                   'country_code': r'^.{0,10}$',
                   }

    def __init__(self, address, city, postal_code,
                 first_name=None, last_name=None, phone=None,
                 country_code=None):

        self.address = address
        self.city = city
        self.postal_code = postal_code
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.country_code = country_code

        super(Address, self).__init__()
