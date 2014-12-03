import unittest

from faker import Faker

from veritranspay import request, validators, payment_types
from veritranspay.veritrans import VTDirect
from . import dummy_data


fake = Faker()


class VTDirect_Init_Tests(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.server_key = fake.word()
        super(VTDirect_Init_Tests, self).setUp()

    def test_requires_server_key(self):
        ''' server_key should be a required parameter. '''
        self.assertRaises(TypeError, VTDirect)

    def test_instance_attributes_set(self):
        v = VTDirect(server_key=self.server_key)
        self.assertEqual(v.server_key, self.server_key, "")
        self.assertFalse(v.sandbox_mode, "")

    def test_sanbox_mode_set_as_attribute(self):
        v = VTDirect(server_key=self.server_key, sandbox_mode=True)
        self.assertEqual(v.server_key, self.server_key, "")
        self.assertTrue(v.sandbox_mode, "")

    def test_sandbox_mode_expected_url(self):
        expected_url = 'https://api.sandbox.veritranspay.co.id/v2'
        v = VTDirect(server_key=self.server_key, sandbox_mode=True)
        self.assertEqual(v.base_url, expected_url)

    def test_live_mode_expected_url(self):
        expected_url = 'https://api.veritranspay.co.id/v2'
        v = VTDirect(server_key=self.server_key, sandbox_mode=False)
        self.assertEqual(v.base_url, expected_url)

    def test_cc_serialization(self):
        ''' Given a complete request format--make sure that our ChargeRequest
        is serializing out the same format.
        '''
        expected = dummy_data.CC_REQUEST

        cc_payment = payment_types.CreditCard(
            bank=expected['credit_card']['bank'],
            token_id=expected['credit_card']['token_id'])
        trans_details = request.TransactionDetails(
            order_id=expected['transaction_details']['order_id'],
            gross_amount=expected['transaction_details']['gross_amount'])
        cust_details = request.CustomerDetails(
            first_name=expected['customer_details']['first_name'],
            last_name=expected['customer_details']['last_name'],
            email=expected['customer_details']['email'],
            phone=expected['customer_details']['phone'],
            billing_address=request.Address(
                **expected['customer_details']['billing_address']),
            shipping_address=request.Address(
                **expected['customer_details']['shipping_address'])
            )
        item_details = [request.ItemDetails(item_id=item['id'],
                                            price=item['price'],
                                            quantity=item['quantity'],
                                            name=item['name'])
                        for item
                        in expected['item_details']]

        charge_req = request.ChargeRequest(charge_type=cc_payment,
                                           transaction_details=trans_details,
                                           customer_details=cust_details,
                                           item_details=item_details)

        actual = charge_req.serialize()

        self.assertEqual(actual, expected)

