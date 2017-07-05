import random
import unittest
import os

import requests
from requests import codes

import veritranspay
from veritranspay import request, veritrans, payment_types, response
from veritranspay.response import status

from . import fixtures
from faker import Faker
fake = Faker()

SANDBOX_CLIENT_KEY = os.environ.get('SANDBOX_CLIENT_KEY', None)
SANDBOX_SERVER_KEY = os.environ.get('SANDBOX_SERVER_KEY', None)
RUN_ALL_ACCEPTANCE_TESTS = os.environ.get('RUN_ALL_ACCEPTANCE_TESTS', False)


class LiveTests_Base(object):

    def setUp(self):

        if None in [SANDBOX_CLIENT_KEY, SANDBOX_SERVER_KEY]:
            self.skipTest("Live credentials not provided -- skipping tests")
        if not RUN_ALL_ACCEPTANCE_TESTS and \
                self.VERSION != veritranspay.__version__:
            self.skipTest("Skipping this version of tests")

        expected = fixtures.CC_REQUEST
        self.expected = expected

        self.trans_details = request.TransactionDetails(
            order_id=expected['transaction_details']['order_id'],
            gross_amount=expected['transaction_details']['gross_amount'])

        self.cust_details = request.CustomerDetails(
            first_name=expected['customer_details']['first_name'],
            last_name=expected['customer_details']['last_name'],
            email=expected['customer_details']['email'],
            phone=expected['customer_details']['phone'],
            billing_address=request.Address(
                **expected['customer_details']['billing_address']),
            shipping_address=request.Address(
                **expected['customer_details']['shipping_address'])
            )

        self.item_details = \
            [request.ItemDetails(item_id=item['id'],
                                 price=item['price'],
                                 quantity=item['quantity'],
                                 name=item['name'])
             for item
             in expected['item_details']]

    def get_token(self, cc_num, client_key, secure=False):
        # try to get a token
        params = {'card_number': cc_num,
                  'card_exp_month': '12',
                  'card_exp_year': '2020',
                  'card_cvv': '123',
                  'secure': secure,
                  'gross_amount': 145000,
                  'client_key': client_key,
                  }
        token_url = 'https://api.sandbox.midtrans.com/v2/token'
        resp = requests.get(token_url, params=params)

        if resp.status_code == codes.OK:
            return resp.json()['token_id']
        else:
            self.fail("Failed retrieving token from server")


class AcceptanceTests_v0_4(LiveTests_Base, unittest.TestCase):

    VERSION = 'v0.4'

    def test_success_cc_charge_request(self):

        # 1: get a token
        # on live, this step --MUST-- be performed by the web
        # application through the javascript library.
        token = self.get_token(
            random.choice(fixtures.CC_ACCEPTED),
            SANDBOX_CLIENT_KEY)

        # 2: Create a sandbox gateway
        gateway = veritrans.VTDirect(
            SANDBOX_SERVER_KEY,
            sandbox_mode=True)

        # 3: Create a charge request
        cc_payment = payment_types.CreditCard(
            bank=self.expected['credit_card']['bank'],
            token_id=token)

        charge_req = request.ChargeRequest(
            charge_type=cc_payment,
            transaction_details=self.trans_details,
            customer_details=self.cust_details,
            item_details=self.item_details)

        # 4: Submit our request
        resp = gateway.submit_charge_request(charge_req)

        self.assertIsInstance(resp, response.CreditCardChargeResponse)
        self.assertEqual(status.SUCCESS, resp.status_code)


class AcceptanceTests_v0_5(LiveTests_Base, unittest.TestCase):
    VERSION = 'v0.5'
    def test_accept_challenged_charge_request(self):
        '''
        Verify that we can accept challenged charge requests.
        '''
        # 1: get a token
        # on live, this step --MUST-- be performed by the web
        # application through the javascript library.
        token = self.get_token(
            random.choice(fixtures.CC_CHALLENGED_FDS),
            SANDBOX_CLIENT_KEY)

        # 2: Create a sandbox gateway
        gateway = veritrans.VTDirect(
            SANDBOX_SERVER_KEY,
            sandbox_mode=True)

        # 3: Create a charge request
        cc_payment = payment_types.CreditCard(
            bank=self.expected['credit_card']['bank'],
            token_id=token)

        charge_req = request.ChargeRequest(
            charge_type=cc_payment,
            transaction_details=self.trans_details,
            customer_details=self.cust_details,
            item_details=self.item_details)

        # 4: Submit charge request
        #     - verify we get a status_code of CHALLENGE back
        #     - verify that we are returned a CreditCardChargeResponse
        resp = gateway.submit_charge_request(charge_req)

        self.assertIsInstance(resp, response.CreditCardChargeResponse)
        self.assertEqual(status.CHALLENGE, resp.status_code)

        # 5: Lookup the status of the transaction using the response
        #     - verify can use CreditCareChargeResponse can as a StatusRequest
        #     - verify we get a StatusResponse back
        #     - verify the status_code is still CHALLENGE
        status_resp = gateway.submit_status_request(resp)
        self.assertIsInstance(status_resp, response.StatusResponse)
        self.assertEqual(status_resp.status_code, status.CHALLENGE)

        # 6: Approve the transaction!
        #     - verify can build an ApprovalRequest
        #     - verify we get an ApprovalResponse back
        #     - verify the status_code is now SUCCESS
        approval_req = request.ApprovalRequest(
            status_resp.order_id)
        approval_resp = gateway.submit_approval_request(
            approval_req)

        self.assertIsInstance(approval_resp, response.ApproveResponse)
        self.assertEqual(approval_resp.status_code, status.SUCCESS)


class AcceptanceTests_v0_6(LiveTests_Base, unittest.TestCase):

    def test_one_click(self):
        pass

    def test_two_click(self):
        pass

    def test_preauth_capture(self):
        pass


class PermataVA_AcceptanceTests_v0_8(unittest.TestCase):

    VERSION = '0.8'

    def setUp(self):
        if None in [SANDBOX_CLIENT_KEY, SANDBOX_SERVER_KEY]:
            self.skipTest("Live credentials not provided -- skipping tests")

        if not RUN_ALL_ACCEPTANCE_TESTS and \
                self.VERSION != veritranspay.__version__:
            self.skipTest("Skipping %s this version of tests" % (self.VERSION))

        expected = fixtures.VIRTUALACCOUNTPERMATA_REQUEST
        self.expected = expected

        self.trans_details = request.TransactionDetails(
            order_id=expected['transaction_details']['order_id'],
            gross_amount=expected['transaction_details']['gross_amount'])

        self.cust_details = request.CustomerDetails(
            first_name=expected['customer_details']['first_name'],
            last_name=expected['customer_details']['last_name'],
            email=expected['customer_details']['email'],
            phone=expected['customer_details']['phone'],
            billing_address=request.Address(
                **expected['customer_details']['billing_address']),
            shipping_address=request.Address(
                **expected['customer_details']['shipping_address'])
            )
        self.item_details = \
            [request.ItemDetails(item_id=item['id'],
                                 price=item['price'],
                                 quantity=item['quantity'],
                                 name=item['name'])
             for item
             in expected['item_details']]

    def test_virtualaccountpermata(self):
        """
        Verify Permata Virtual Account
        """

        trans_details = self.trans_details
        trans_details.order_id = "".join([fake.random_letter() for _ in range(10)])

        # 2: Create a sandbox gateway
        gateway = veritrans.VTDirect(
            SANDBOX_SERVER_KEY,
            sandbox_mode=True)

        # 3: Create a charge request
        payment = payment_types.VirtualAccountPermata()

        charge_req = request.ChargeRequest(
            charge_type=payment,
            transaction_details=trans_details,
            customer_details=self.cust_details,
            item_details=self.item_details)

        # 4: Submit our request
        resp = gateway.submit_charge_request(charge_req)

        self.assertIsInstance(resp, response.VirtualAccountPermataChargeResponse)
        self.assertEqual(status.PENDING, resp.status_code)
        self.assertEqual(self.trans_details.order_id, resp.order_id)


class BriEpay_AcceptanceTests_v0_8(unittest.TestCase):

    VERSION = '0.8'

    def setUp(self):
        if None in [SANDBOX_CLIENT_KEY, SANDBOX_SERVER_KEY]:
            self.skipTest("Live credentials not provided -- skipping tests")

        if not RUN_ALL_ACCEPTANCE_TESTS and \
                self.VERSION != veritranspay.__version__:
            self.skipTest("Skipping %s this version of tests" % self.VERSION)

        expected = fixtures.BRIEPAY_REQUEST
        self.expected = expected

        self.trans_details = request.TransactionDetails(
            order_id=expected['transaction_details']['order_id'],
            gross_amount=expected['transaction_details']['gross_amount'])

        self.cust_details = request.CustomerDetails(
            first_name=expected['customer_details']['first_name'],
            last_name=expected['customer_details']['last_name'],
            email=expected['customer_details']['email'],
            phone=expected['customer_details']['phone'],
            billing_address=request.Address(
                **expected['customer_details']['billing_address']),
            shipping_address=request.Address(
                **expected['customer_details']['shipping_address'])
            )
        self.item_details = \
            [request.ItemDetails(item_id=item['id'],
                                 price=item['price'],
                                 quantity=item['quantity'],
                                 name=item['name'])
             for item
             in expected['item_details']]

    def test_briepay(self):
        """
            Verify Bri Epay payment method
        """
        # 2: Create a sandbox gateway
        gateway = veritrans.VTDirect(
            SANDBOX_SERVER_KEY,
            sandbox_mode=True)

        # 3: Create a charge request
        payment = payment_types.BriEpay()

        charge_req = request.ChargeRequest(
            charge_type=payment,
            transaction_details=self.trans_details,
            customer_details=self.cust_details,
            item_details=self.item_details)

        # 4: Submit our request
        resp = gateway.submit_charge_request(charge_req)

        self.assertIsInstance(resp, response.EpayBriChargeResponse)
        self.assertEqual(status.PENDING, resp.status_code)
        self.assertEqual(self.trans_details.order_id, resp.order_id)


class MandiriVA_AcceptanceTests_v0_8(unittest.TestCase):

    VERSION = '0.8'

    def setUp(self):
        if None in [SANDBOX_CLIENT_KEY, SANDBOX_SERVER_KEY]:
            self.skipTest("Live credentials not provided -- skipping tests")

        if not RUN_ALL_ACCEPTANCE_TESTS and \
                self.VERSION != veritranspay.__version__:
            self.skipTest("Skipping %s this version of tests" % self.VERSION)

        expected = fixtures.VIRTUALACCOUNTMANDIRI_REQUEST
        self.expected = expected

        self.trans_details = request.TransactionDetails(
            order_id="".join([fake.random_letter() for _ in range(10)]),
            gross_amount=expected['transaction_details']['gross_amount'])

        self.cust_details = request.CustomerDetails(
            first_name=expected['customer_details']['first_name'],
            last_name=expected['customer_details']['last_name'],
            email=expected['customer_details']['email'],
            phone=expected['customer_details']['phone'],
            billing_address=request.Address(
                **expected['customer_details']['billing_address']),
            shipping_address=request.Address(
                **expected['customer_details']['shipping_address'])
            )
        self.item_details = \
            [request.ItemDetails(item_id=item['id'],
                                 price=item['price'],
                                 quantity=item['quantity'],
                                 name=item['name'])
             for item
             in expected['item_details']]

    def test_virtual_account_mandiri(self):
        """
        Verify mandiri bill payment
        :return:
        """

        # 2: Create a sandbox gateway
        gateway = veritrans.VTDirect(
            SANDBOX_SERVER_KEY,
            sandbox_mode=True)

        # 3: Create a charge request
        payment = payment_types.VirtualAccountMandiri(bill_info1=self.expected['echannel']['bill_info1'], bill_info2=self.expected['echannel']['bill_info2'])

        charge_req = request.ChargeRequest(
            charge_type=payment,
            transaction_details=self.trans_details,
            customer_details=self.cust_details,
            item_details=self.item_details)

        # 4: Submit our request
        resp = gateway.submit_charge_request(charge_req)

        self.assertIsInstance(resp, response.VirtualAccountMandiriChargeResponse)
        self.assertEqual(status.PENDING, resp.status_code)
        self.assertEqual(self.trans_details.order_id, resp.order_id)
