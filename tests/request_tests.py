'''
Tests the main type of request entities, ChargeRequest, StatusRequest,
AcceptRequest, and CancelRequest
'''
import unittest

from faker import Faker

from midtranspay import request, payment_types, validators

from . import fixtures


fake = Faker()


class ChargeRequest_UnitTests(unittest.TestCase):

    def test_serialization(self):
        '''
        This test covers the serialization of ChargeRequest and all of it's
        subentities.
        '''
        expected = fixtures.CC_REQUEST

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


class StatusRequest_UnitTests(unittest.TestCase):

    def test_init_args_persisted_as_attribues(self):
        order_id = ''.join([fake.random_letter() for _ in range(20)])
        req = request.StatusRequest(order_id)
        self.assertEqual(req.order_id, order_id)

    def test_orderid_max_50_chars(self):
        order_id = ''.join([fake.random_letter() for _ in range(51)])
        req = request.StatusRequest(order_id)
        self.assertRaises(validators.ValidationError,
                          lambda: req.validate_all())


class ApprovalRequest_UnitTests(unittest.TestCase):

    def test_init_args_persisted_as_attribues(self):
        order_id = ''.join([fake.random_letter() for _ in range(20)])
        req = request.ApprovalRequest(order_id)
        self.assertEqual(req.order_id, order_id)

    def invalid_orderid_raises_validation_exception(self):
        order_id = ''.join([fake.random_letter() for _ in range(51)])
        req = request.ApprovalRequest(order_id)
        self.assertRaises(validators.ValidationError,
                          lambda: req.validate_all())


class CancelRequest_UnitTests(unittest.TestCase):

    def test_init_args_persisted_as_attribues(self):
        order_id = ''.join([fake.random_letter() for _ in range(20)])
        req = request.CancelRequest(order_id)
        self.assertEqual(req.order_id, order_id)

    def invalid_orderid_raises_validation_exception(self):
        order_id = ''.join([fake.random_letter() for _ in range(51)])
        req = request.CancelRequest(order_id)
        self.assertRaises(validators.ValidationError,
                          lambda: req.validate_all())
