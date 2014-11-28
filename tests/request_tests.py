import unittest
import random
import string

from faker import Faker

from veritrans import request
from . import dummy_data

fake = Faker()


class Request_Address_Tests(unittest.TestCase):

    def setUp(self):
        self.first_name = fake.first_name()
        self.last_name = fake.last_name()
        self.address = fake.address()
        self.city = fake.city()
        self.postal_code = fake.postcode()
        # note: we can't use fake-factory's phone_number() because
        # it can occasionally include extensions, which veritrans'
        # documentation says they won't accept.
        self.phone = random.choice(dummy_data.PHONE_NUMBERS)
        self.country_code = random.choice(dummy_data.COUNTRY_CODES)

        self.complete_address = request.Address(first_name=self.first_name,
                                                last_name=self.last_name,
                                                address=self.address,
                                                city=self.city,
                                                postal_code=self.postal_code,
                                                phone=self.phone,
                                                country_code=self.country_code)

        super(Request_Address_Tests, self).setUp()

    def test_init_sets_attributes(self):
        ''' Make sure __init__ is persisting it's arguments
        as instance attributes.
        '''
        addr = request.Address(first_name=self.first_name,
                               last_name=self.last_name,
                               address=self.address,
                               city=self.city,
                               postal_code=self.postal_code,
                               phone=self.phone,
                               country_code=self.country_code)

        self.assertEqual(addr.first_name, self.first_name)
        self.assertEqual(addr.last_name, self.last_name)
        self.assertEqual(addr.address, self.address)
        self.assertEqual(addr.city, self.city)
        self.assertEqual(addr.postal_code, self.postal_code)
        self.assertEqual(addr.phone, self.phone)
        self.assertEqual(addr.country_code, self.country_code)

    def test_init_args_with_defaults(self):
        ''' Make sure that our init args that have default values are
        set as attributes on the instance with their expected values
        '''
        addr = request.Address(address=self.address,
                               city=self.city,
                               postal_code=self.postal_code)

        self.assertEqual(addr.address, self.address)
        self.assertEqual(addr.city, self.city)
        self.assertEqual(addr.postal_code, self.postal_code)

        self.assertEqual(addr.first_name, None)
        self.assertEqual(addr.last_name, None)
        self.assertEqual(addr.phone, None)
        self.assertEqual(addr.country_code, None)

    def test_validation_address(self):

        pattern = request.Address._validators['address']
        addr = self.complete_address

        # this shouldn't throw an exception
        valid_address = fake.address()
        self.assertIsNone(
            addr.validate_attr('address',
                               valid_address,
                               pattern))

        # these two addresses should raise exceptions
        bad_blank_address = ''
        bad_long_address = ''.join(
            random.choice(string.ascii_letters) for _ in range(201))

        for bad_addr in [bad_blank_address, bad_long_address]:
            l = lambda: addr.validate_attr('address',
                                           bad_addr,
                                           pattern)
            self.assertRaises(ValueError, l)

    def test_validation_city(self):

        pattern = request.Address._validators['city']
        addr = self.complete_address

        # should return without issue
        valid_city = fake.city()
        self.assertIsNone(addr.validate_attr('city',
                                             valid_city,
                                             pattern))

        # invalid values should raise ValueErrors
        bad_blank_city = ''
        bad_long_city = ''.join(
            random.choice(string.ascii_letters) for _ in range(21))

        for bad in [bad_blank_city, bad_long_city]:
            l = lambda: addr.validate_attr('city',
                                           bad,
                                           pattern)
            self.assertRaises(ValueError, l)

    def test_validation_postal_code(self):

        pattern = request.Address._validators['postal_code']
        addr = self.complete_address

        # should return without issue
        valid_pc = fake.postcode()
        self.assertIsNone(addr.validate_attr('postal_code',
                                             valid_pc,
                                             pattern))

        # invalid values should raise ValueErrors
        bad_blank_city = ''
        bad_long_city = ''.join(
            random.choice(string.digits) for _ in range(11))

        for bad in [bad_blank_city, bad_long_city]:
            l = lambda: addr.validate_attr('postal_code',
                                           bad,
                                           pattern)
            self.assertRaises(ValueError, l)

    def test_validation_first_name(self):

        pattern = request.Address._validators['first_name']
        addr = self.complete_address

        # should return without issue
        valid_name = fake.first_name()
        valid_blank_name = ''

        for valid in [valid_name, valid_blank_name]:
            self.assertIsNone(addr.validate_attr('first_name',
                                                 valid,
                                                 pattern))

        # invalid values should raise ValueErrors
        bad_long_name = ''.join(
            random.choice(string.ascii_letters) for _ in range(21))

        for bad in [bad_long_name]:
            l = lambda: addr.validate_attr('first_name',
                                           bad,
                                           pattern)
            self.assertRaises(ValueError, l)

    def test_validation_last_name(self):
        pattern = request.Address._validators['last_name']
        addr = self.complete_address

        # should return without issue
        valid_name = fake.last_name()
        valid_blank_name = ''

        for valid in [valid_name, valid_blank_name]:
            self.assertIsNone(addr.validate_attr('last_name',
                                                 valid,
                                                 pattern))

        # invalid values should raise ValueErrors
        bad_long_name = ''.join(
            random.choice(string.ascii_letters) for _ in range(21))

        for bad in [bad_long_name]:
            l = lambda: addr.validate_attr('last_name',
                                           bad,
                                           pattern)
            self.assertRaises(ValueError, l)

    def test_validation_phone_number(self):
        pattern = request.Address._validators['phone']
        addr = self.complete_address

        # should return without issue
        valid_phone = '+1(330) 776-8177'
        valid_blank_phone = ''

        for valid in [valid_phone, valid_blank_phone]:
            self.assertIsNone(addr.validate_attr('phone',
                                                 valid,
                                                 pattern))

        # invalid values should raise ValueErrors
        for bad in ['1234', 'asdflkjasdf', '2239847293847928374234234']:
            l = lambda: addr.validate_attr('phone',
                                           bad,
                                           pattern)
            self.assertRaises(ValueError, l)

    def test_validation_country_code(self):
        pattern = request.Address._validators['country_code']
        addr = self.complete_address

        # should return without issue
        for valid in ['USA', 'IDN', '']:
            self.assertIsNone(addr.validate_attr('country_code',
                                                 valid,
                                                 pattern))

        # invalid values should raise ValueErrors
        for bad in ['IDNINDINDIND', '2239847293847928374234234']:
            l = lambda: addr.validate_attr('country_code',
                                           bad,
                                           pattern)
            self.assertRaises(ValueError, l)
