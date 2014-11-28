import unittest
import random

from faker import Faker
from mock import MagicMock

from veritrans import request
from . import dummy_data

fake = Faker()


class Request_CustomerDetails_UnitTests(unittest.TestCase):

    def setUp(self):

        self.first_name = fake.first_name()
        self.last_name = fake.last_name()
        self.email = fake.email()
        self.phone = random.choice(dummy_data.PHONE_NUMBERS)

        self.complete_cd = request.CustomerDetails(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            phone=self.phone)

        super(Request_CustomerDetails_UnitTests, self).setUp()

    def test_init_sets_attrs(self):
        ''' Make sure that init is setting all it's attributes properly.
        '''
        cd = request.CustomerDetails(first_name=self.first_name,
                                     last_name=self.last_name,
                                     email=self.email,
                                     phone=self.phone)

        self.assertEqual(cd.first_name, self.first_name)
        self.assertEqual(cd.last_name, self.last_name)
        self.assertEqual(cd.email, self.email)
        self.assertEqual(cd.phone, self.phone)

    def test_init_addrs_default_none(self):

        cd = request.CustomerDetails(first_name=self.first_name,
                                     last_name=self.last_name,
                                     email=self.email,
                                     phone=self.phone)

        self.assertIsNone(cd.billing_address)
        self.assertIsNone(cd.shipping_address)

    def test_validate_first_name(self):

        cd = self.complete_cd
        pattern = request.CustomerDetails._validators['first_name']

        self.assertIsNone(cd.validate_attr('first_name',
                                           self.first_name,
                                           pattern))

        bad_blank = ''
        bad_long = ''.join([fake.random_letter() for _ in range(21)])

        for bad in [bad_blank, bad_long]:
            l = lambda: cd.validate_attr('first_name', bad, pattern)
            self.assertRaises(ValueError, l)

    def test_validate_last_name(self):

        cd = self.complete_cd
        pattern = request.CustomerDetails._validators['last_name']

        valid_name = self.last_name
        valid_blank = ''
        for valid in [valid_name, valid_blank]:
            self.assertIsNone(cd.validate_attr('last_name',
                                               valid,
                                               pattern))

        bad_long = ''.join([fake.random_letter() for _ in range(21)])
        for bad in [bad_long]:
            l = lambda: cd.validate_attr('last_name', bad, pattern)
            self.assertRaises(ValueError, l)

    def test_validate_email_name(self):

        cd = self.complete_cd
        pattern = request.CustomerDetails._validators['email']

        self.assertIsNone(cd.validate_attr('email',
                                           self.email,
                                           pattern))

        # bad_email = 'a-am-not-an-email'
        long_email = "".join(fake.random_letter() for _ in range(46))

        for bad in [long_email]:
            l = lambda: cd.validate_attr('email', bad, pattern)
            self.assertRaises(ValueError, l)

    def test_valid_phone(self):

        cd = self.complete_cd
        pattern = request.CustomerDetails._validators['phone']

        self.assertIsNone(cd.validate_attr('phone',
                                           self.phone,
                                           pattern))

        # todo: replace validation mechanism with lambdas and test validators

    def test_billing_address(self):
        pass

    def test_valid_shipping_address(self):
        pass
