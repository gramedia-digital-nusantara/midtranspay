import random
import unittest
import os

import requests
from requests import codes

from faker import Faker
fake = Faker()

import veritranspay
from veritranspay import request, veritrans, payment_types, response
from veritranspay.response import status

from . import fixtures


SANDBOX_CLIENT_KEY = os.environ.get('SANDBOX_CLIENT_KEY', None)
SANDBOX_SERVER_KEY = os.environ.get('SANDBOX_SERVER_KEY', None)
RUN_ALL_ACCEPTANCE_TESTS = os.environ.get('RUN_ALL_ACCEPTANCE_TESTS', False)


class InternetBankingTests_Base(object):

    def setUp(self):
        if None in [SANDBOX_CLIENT_KEY, SANDBOX_SERVER_KEY]:
            self.skipTest("Live credentials not provided -- skipping tests")
        if not RUN_ALL_ACCEPTANCE_TESTS and \
                self.VERSION != veritranspay.__version__:
            self.skipTest("Skipping this version of tests")

        expected = fixtures.CC_REQUEST
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


class MandiriClickpayTests_v0_9(InternetBankingTests_Base, unittest.TestCase):

    VERSION = '0.9'

    def test_mandiri_click_pay_charge(self):
        # 1: Create a sandbox gateway
        gateway = veritrans.VTDirect(
            server_key=SANDBOX_SERVER_KEY,
            sandbox_mode=True)

        # 2: Set payment type Internet Banking from Mandiri Click pay
        mandiri_clickpay = payment_types.MandiriClickpay(
            card_number="4111111111111111",
            input1="1111111111",
            input2="145000",
            input3="54321",
            token="000000")

        # 3: Create a charge request
        charge_req = request.ChargeRequest(
            charge_type=mandiri_clickpay,
            transaction_details=self.trans_details,
            customer_details=self.cust_details,
            item_details=self.item_details)

        # 4: Submit our request
        resp = gateway.submit_charge_request(charge_req)

        self.assertIsInstance(resp, response.MandiriChargeResponse)
        self.assertEqual(status.SUCCESS, resp.status_code)


class CimbClicksTests_v0_9(InternetBankingTests_Base, unittest.TestCase):

    VERSION = '0.9'

    def test_cimb_clicks_charge(self):
        # 1: Create a sandbox gateway
        gateway = veritrans.VTDirect(
            server_key=SANDBOX_SERVER_KEY,
            sandbox_mode=True)

        # 2: Set payment type to Cimb Clicks internet banking.
        cimb_clicks = payment_types.CimbClicks(
            description="Purchase of a special event item")

        # 3: Create a charge request
        charge_req = request.ChargeRequest(
            charge_type=cimb_clicks,
            transaction_details=self.trans_details,
            customer_details=self.cust_details,
            item_details=self.item_details)

        # 4: Submit our request
        resp = gateway.submit_charge_request(charge_req)

        self.assertIsInstance(resp, response.CimbsChargeResponse)
        self.assertEqual(status.CHALLENGE, resp.status_code)


class BCAKlikPayTests_v0_9(InternetBankingTests_Base, unittest.TestCase):

    VERSION = '0.9'

    def test_bcaklikpay_charger(self):
        # 1: Create a sandbox gateway
        gateway = veritrans.VTDirect(
            server_key=SANDBOX_SERVER_KEY,
            sandbox_mode=True)

        # 2: Set Internet banking BCA Klik pay
        bca_klikpay = payment_types.BCAKlikPay(type_id=1, description="Pembelian barang")

        # 3: Create a charge request
        charge_req = request.ChargeRequest(
            charge_type=bca_klikpay,
            transaction_details=self.trans_details,
            customer_details=self.cust_details,
            item_details=self.item_details)

        # 4: Submit our request
        resp = gateway.submit_charge_request(charge_req)

        self.assertIsInstance(resp, response.BCAKlikPayChargeResponse)
        self.assertEqual(status.CHALLENGE, resp.status_code)


class KlikBCATests_v0_9(InternetBankingTests_Base, unittest.TestCase):

    VERSION = '0.9'

    def test_klikbca_charger(self):
        # 1: Create a sandbox gateway
        gateway = veritrans.VTDirect(
            server_key=SANDBOX_SERVER_KEY,
            sandbox_mode=True)

        # 2: Set Internet banking Klik BCA
        klik_bca = payment_types.KlikBCA(user_id="midtrans1014", # error
                                         description="Testing transaction")

        # 3: Create a charge request
        charge_req = request.ChargeRequest(
            charge_type=klik_bca,
            transaction_details=self.trans_details,
            customer_details=self.cust_details,
            item_details=self.item_details)

        # 4: Submit our request
        resp = gateway.submit_charge_request(charge_req)

        self.assertIsInstance(resp, response.KlikBCAChargeResponse)
        self.assertEqual(status.CHALLENGE, resp.status_code)

