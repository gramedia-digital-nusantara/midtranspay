'''
Contains sub-entities that are used to create a complete
charge request to the Veritrans API.

http://docs.veritrans.co.id/sandbox/charge.html#specification
'''

from . import mixins, validators


class Address(mixins.ValidatableMixin, mixins.SerializableMixin):

    _validators = {'address': r'^(.{1,200})$',
                   'city': r'^(.{1,20})$',
                   'postal_code': validators.POSTALCODE_REQUIRED,
                   'first_name': validators.NAME_OPTIONAL,
                   'last_name': validators.NAME_OPTIONAL,
                   'phone': validators.PHONE_OPTIONAL,
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


class TransactionDetails(mixins.ValidatableMixin, mixins.SerializableMixin):

    _validators = {'order_id': r'^.{1,50}$',
                   'gross_amount': validators.DUMMY_VALIDATOR,
                   }

    def __init__(self, order_id, gross_amount):
        self.order_id = order_id
        self.gross_amount = gross_amount

    def validate_attr(self, name, value, pattern):
        # note: one of 3 numeric elements, so manually providing validation
        if name == 'gross_amount':
            if not type(value) in [int, float, long]:
                raise ValueError()
        else:
            super(TransactionDetails, self).validate_attr(name,
                                                          value,
                                                          pattern)


class CustomerDetails(mixins.ValidatableMixin, mixins.SerializableMixin):

    _validators = {'first_name': validators.NAME_REQUIRED,
                   'last_name': validators.NAME_OPTIONAL,
                   'email': validators.EMAIL_REQUIRED,
                   'phone': validators.PHONE_REQUIRED,
                   'billing_address': validators.DUMMY_VALIDATOR,
                   'shipping_address': validators.DUMMY_VALIDATOR,
                   }

    def __init__(self, first_name, last_name, email, phone,
                 billing_address=None, shipping_address=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.billing_address = billing_address
        self.shipping_address = shipping_address


class ChargeRequest(object):

    def __init__(self, charge_type, transaction_details, customer_details,
                 item_details=[]):
        self.charge_type = charge_type
        self.transaction_details = transaction_details
        self.customer_details = customer_details
        self.item_details = item_details

    def serialize(self):
        rv = {}
        rv.update(self.charge_type)
        rv.update(self.transaction_details)
        rv.update(self.customer_details)
        if self.item_details:
            rv.update({'item_details': self.item_details})
        return rv
