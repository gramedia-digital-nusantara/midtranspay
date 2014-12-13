'''
Contains entities and sub-entities that are used to create a complete
charge request to the Veritrans API.

http://docs.veritranspay.co.id/sandbox/charge.html#specification
'''
from . import mixins, validators, constraints


class Address(mixins.RequestEntity):
    '''
    Address is a subcomponent of CustomerDetails.
    Represents a physical address in some way associated with the customer,
    either their 'billing address' or their 'mailing address'
    '''
    _validators = {'address': validators.AddressValidator(),
                   'city': validators.CityValidator(),
                   'postal_code': validators.PostalcodeValidator(),
                   'first_name': validators.NameValidator(is_required=False),
                   'last_name': validators.NameValidator(is_required=False),
                   'phone': validators.PhoneValidator(is_required=False),
                   'country_code': validators.CountrycodeValidator(
                       is_required=False),
                   }

    def __init__(self, address, city, postal_code,
                 first_name=None, last_name=None, phone=None,
                 country_code=None):
        '''
        Creates a new instance of Address.

        :param address: REQUIRED - Maximum 200 characters.
        :param city: REQUIRED - Maximum 20 characters.
        :param postal_code: REQUIRED - Maximum 10 digits, including '-' and spaces.
        :param first_name: Maximum 20 characters.
        :param last_name: Maximum 20 characters
        :param phone: 5-19 characters (if provided).
        :param country_code: Maximum 10 characters.  Should be in ISO-3166 alpha-3
        '''
        self.address = address
        self.city = city
        self.postal_code = postal_code
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.country_code = country_code


class TransactionDetails(mixins.RequestEntity):
    '''
    Subcomponent of ChargeRequest.  Indicates a order_id that is provided
    by the calling code, and a gross_amount indicating the total charge amount
    in IDR.
    '''
    _validators = {'order_id': validators.StringValidator(
                        max_length=constraints.MAX_ORDERID_LENGTH),
                   'gross_amount': validators.NumericValidator(),
                   }

    def __init__(self, order_id, gross_amount):
        '''
        Creates a new instance of TransactionDetails.

        :param order_id: REQUIRED - Maximum 50 characters.
        :param gross_amount: REQUIRED - Numeric value to represent the charge amount.
        '''
        self.order_id = order_id
        self.gross_amount = gross_amount


class CustomerDetails(mixins.RequestEntity):
    '''
    Information about the customer making the purchase.
    '''
    _validators = {'first_name': validators.NameValidator(),
                   'last_name': validators.NameValidator(is_required=False),
                   'email': validators.EmailValidator(),
                   'phone': validators.PhoneValidator(),
                   'billing_address': validators.DummyValidator(),
                   'shipping_address': validators.DummyValidator(),
                   }

    def __init__(self, first_name, last_name, email, phone,
                 billing_address=None, shipping_address=None):
        '''
        Creates a new CustomerDetails instance.

        :param first_name: REQUIRED - Maximum 20 characters.
        :param last_name: Maximum 20 characters.
        :param email: REQUIRED - Maximum 45 characters.
        :param phone: REQUIRED - 5-19 characters.
        :param billing_address: Address object instance.
        :param shipping_address: Address object instance.
        '''
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.billing_address = billing_address
        self.shipping_address = shipping_address


class ItemDetails(mixins.RequestEntity):
    '''
    Line items details for a transaction.
    '''
    # todo: yo tests

    _validators = {'id': validators.StringValidator(max_length=50),
                   'price': validators.NumericValidator(),
                   'quantity': validators.NumericValidator(),
                   'name': validators.StringValidator(max_length=50),
                   }

    def __init__(self, item_id, price, quantity, name):
        self.id = item_id
        self.price = price
        self.quantity = quantity
        self.name = name


class ChargeRequest(mixins.RequestEntity):
    '''
    Encapsulates the 4 other entity types that are involved with submitting
    a charge request to Veritrans.
    '''
    _validators = {'charge_type': validators.DummyValidator(),
                   'transaction_details': validators.PassthroughValidator(),
                   'customer_details': validators.PassthroughValidator(),
                   'item_details': validators.PassthroughValidator(),
                   }

    def __init__(self, charge_type, transaction_details, customer_details,
                 item_details=[]):
        self.charge_type = charge_type
        self.transaction_details = transaction_details
        self.customer_details = customer_details
        self.item_details = item_details

    def validate_attr(self, name, value, validator):
        '''
        Manually overrides validation logic for items, since they're a list
        type and this is a special case.  Everything else can be validated
        normally.
        '''
        if 'name' == 'item_details':
            for item in self.item_details:
                item.validate_all()
        else:
            super(ChargeRequest, self).validate_attr(name, value, validator)

    def serialize(self):
        '''
        Manually override the standard logic for serialize().  `charge_type`
        needs to add two keys to the resulting dictionary, and all other types
        need to be placed under specific dictionary keys.
        '''
        rv = {}
        rv.update(self.charge_type.serialize())
        rv.update({'transaction_details':
                   self.transaction_details.serialize()})
        rv.update({'customer_details': self.customer_details.serialize()})
        if self.item_details:
            rv.update({'item_details': [item.serialize() for item
                                        in self.item_details]})
        return rv
