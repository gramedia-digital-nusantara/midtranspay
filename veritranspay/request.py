'''
Contains entities and sub-entities that are used to create a complete
charge request to the Veritrans API.

http://docs.veritranspay.co.id/sandbox/charge.html#specification
'''
from . import mixins, validators, constraints


class Address(mixins.RequestEntity):
    '''
    Represents a physical address somewhere in the world.
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
        :param address: Street address.
        :type address: :py:class:`str` <= 200
        :param city:  City name.
        :type city: :py:class:`str` <= 20.
        :param postal_code: Postal Code.
        :type postal_code: :py:class:`str` <= 10; numbers, hyphens '-',
            and spaces ' '
        :param first_name: Person given name.
        :type first_name: :py:class:`str` <= 20.
        :param last_name: Person surname.
        :type last_name: :py:class:`str` <= 20.
        :param phone: Phone number.
        :type phone: :py:class:`str` 5 >=< 19; numbers,
            hyphens '-', parenthesis '()',
            spaces ' '; can start with plus symbol '+'
        :param country_code: ISO-3166 alpha-3 country code.
        :type country_code: :py:class:`str` <= 10
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
    Basic information about a transaction with a customer, including
    the order id and the total amount the customer should be charged.
    '''
    _validators = {'order_id':
                   validators.StringValidator(
                       max_length=constraints.MAX_ORDERID_LENGTH),
                   'gross_amount': validators.NumericValidator(),
                   }

    def __init__(self, order_id, gross_amount):
        '''
        :param order_id: **UNIQUE** order identifier.
        :type order_id: :py:class:`str` <= 50
        :param gross_amount: Total amount the customer will be charged.
        :type gross_amount: :py:class:`int`
        '''
        self.order_id = order_id
        self.gross_amount = gross_amount


class CustomerDetails(mixins.RequestEntity):
    '''
    Personal information about a customer.
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
        :param first_name: Person given name.
        :type first_name: :py:class:`str` <= 20.
        :param last_name: Person surname.
        :type last_name: :py:class:`str` <= 20.
        :param email: Person's contact e-mail address.
        :type email: :py:class:`str` <= 45;  Must be a valid e-mail.
        :type phone: :py:class:`str` 5 >=< 19; numbers,
            hyphens '-', parenthesis '()',
            spaces ' '; can start with plus symbol '+'
        :param billing_address: Address used to validate the charge.
        :type billing_address: :py:class:`veritranspay.request.Address`
        :param shipping_address: Address where order should be shipped.
        :type shipping_address: :py:class:`veritranspay.request.Address`
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
    _validators = {'id': validators.StringValidator(max_length=constraints.MAX_ITEMID_LENGTH),
                   'price': validators.NumericValidator(),
                   'quantity': validators.NumericValidator(),
                   'name': validators.StringValidator(max_length=constraints.MAX_ITEMNAME_LENGTH)
                   }

    def __init__(self, item_id, price, quantity, name):
        '''
        :param item_id: Identifier for a given item.
        :type item_id: :py:class:`str` <= 50
        :param price: Unit price for a given item.
        :type price: :py:class:`int`
        :param quantity: Number of units purchased.
        :type quantity: :py:class:`int`
        :param name: Human-readable identifier for product.
        :type name: :py:class:`str` <= 50
        '''
        self.id = item_id
        self.price = price
        self.quantity = quantity
        self.name = name


class ChargeRequest(mixins.RequestEntity):
    '''
    All the information sent to Veritrans to request a customer be charged
    for a particular order.
    '''
    _validators = {'charge_type': validators.DummyValidator(),
                   'transaction_details': validators.PassthroughValidator(),
                   'customer_details': validators.PassthroughValidator(),
                   'item_details': validators.PassthroughValidator(),
                   }

    def __init__(self, charge_type, transaction_details, customer_details,
                 item_details=[]):
        '''
        :param charge_type: Account information against which to submit
            the charge.
        :type charge_type: subclass of
            :py:class:`veritranspay.payment_types.PaymentTypeBase`
        :param transaction_details: Details about the charge being submitted,
            such as the total amount to bill.
        :type transaction_details:
            :py:class:`veritranspay.request.TransactionDetails`
        :param customer_details: Personal details about the person
            being billed.
        :type customer_details:
            :py:class:`veritranspay.request.CustomerDetails`
        :param item_details: Line item details for this transaction.
        :type item_details: iterable of
            :py:class:`veritranspay.request.ItemDetails`
        '''
        self.charge_type = charge_type
        self.transaction_details = transaction_details
        self.customer_details = customer_details
        self.item_details = item_details

    def serialize(self):
        # Manually override the standard logic for serialize().  `charge_type`
        # needs to add two keys to the resulting dictionary, and all
        # other types need to be placed under specific dictionary keys.
        rv = {}
        rv.update(self.charge_type.serialize())
        rv.update({'transaction_details':
                   self.transaction_details.serialize()})
        rv.update({'customer_details': self.customer_details.serialize()})
        if self.item_details:
            rv.update({'item_details': [item.serialize() for item
                                        in self.item_details]})
        return rv


class StatusRequest(mixins.ValidatableMixin):
    '''
    Request used to retrieve information about a single charge
    that has already been submitted to Veritrans.
    '''
    _validators = {'order_id':
                   validators.StringValidator(
                       max_length=constraints.MAX_ORDERID_LENGTH),
                   }

    def __init__(self, order_id):
        '''
        :param order_id: The unique order id of the transaction.
        :type order_id: :py:class:`str` <= 50
        '''
        self.order_id = order_id


class CancelRequest(mixins.ValidatableMixin):
    '''
    Cancels a transaction.  This can only be submitted if the transaction
    is currently still pending.
    '''
    _validators = {'order_id':
                   validators.StringValidator(
                       max_length=constraints.MAX_ORDERID_LENGTH),
                   }

    def __init__(self, order_id):
        '''
        :param order_id: The unique order id of the transaction.
        :type order_id: :py:class:`str` <= 50
        '''
        self.order_id = order_id


class ApprovalRequest(mixins.ValidatableMixin):
    '''
    Approves a transaction that is currently in state 'CHALLENGE'.
    '''
    _validators = {'order_id':
                   validators.StringValidator(
                       max_length=constraints.MAX_ORDERID_LENGTH),
                   }

    def __init__(self, order_id):
        '''
        :param order_id: The unique order id of the transaction.
        :type order_id: :py:class:`str` <= 50
        '''
        self.order_id = order_id


class BinsRequest(mixins.ValidatableMixin):
    '''
    Get bin information
    '''
    _validators = {
        'bin_number': validators.NumericValidator()
    }

    def __init__(self, bin_number):
        '''
        :param bin_number: Bin number of the card.
        '''
        self.bin_number = bin_number