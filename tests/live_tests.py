import random
import unittest

import requests
from requests import codes

from veritranspay import request, veritrans, payment_types, response
from veritranspay.response import status

from . import fixtures


class LiveTests(unittest.TestCase):

    def setUp(self):
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

    def get_token(self, cc_num, client_key):
        # try to get a token
        params = {'card_number': cc_num,
                  'card_exp_month': '12',
                  'card_exp_year': '2020',
                  'card_cvv': '123',
                  'secure': False,
                  'gross_amount': 145000,
                  'client_key': client_key,
                  }
        token_url = 'https://api.sandbox.veritrans.co.id/v2/token'
        resp = requests.get(token_url, params=params)

        if resp.status_code == codes.OK:
            return resp.json()['token_id']
        else:
            self.fail("Failed retrieving token from server")

    def test_success_cc_charge_request(self):
        # if no live_credentials module has been provided,
        # then we cannot run these tests
        try:
            from . import live_credentials
        except ImportError:
            self.skipTest("Live credentials not provided -- skipping tests")

        # 1: get a token
        # on live, this step --MUST-- be performed by the web
        # application through the javascript library.
        token = self.get_token(
            random.choice(fixtures.CC_ACCEPTED),
            live_credentials.SANDBOX_CLIENT_KEY)

        # 2: Create a sandbox gateway
        gateway = veritrans.VTDirect(
            live_credentials.SANDBOX_SERVER_KEY,
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

    def test_cc_challenge_request(self):
        # if no live_credentials module has been provided,
        # then we cannot run these tests
        try:
            from . import live_credentials
        except ImportError:
            self.skipTest("Live credentials not provided -- skipping tests")

        # 1: get a token
        # on live, this step --MUST-- be performed by the web
        # application through the javascript library.
        token = self.get_token(
            random.choice(fixtures.CC_CHALLENGED_FDS),
            live_credentials.SANDBOX_CLIENT_KEY)

        # 2: Create a sandbox gateway
        gateway = veritrans.VTDirect(
            live_credentials.SANDBOX_SERVER_KEY,
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
        self.assertEqual(status.CHALLENGE, resp.status_code)

        # 5: Lookup the status of the transaction using the response
        status_resp = gateway.submit_status_request(resp)
        self.assertIsInstance(status_resp, response.StatusResponse)
        self.assertEqual(status_resp.status_code, status.CHALLENGE)

        # 6: Approve the transaction!
        # we're going to build a special object for this
        approval_req = request.ApprovalRequest(
            status_resp.order_id)
        approval_resp = gateway.submit_approval_request(
            approval_req)

        self.assertIsInstance(approval_resp, response.ApproveResponse)
        self.assertEqual(approval_resp.status_code, status.SUCCESS)
