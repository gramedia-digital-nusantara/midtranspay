import unittest
import requests
from requests import codes
from veritranspay import request, veritrans, payment_types
from . import fixtures


class LiveTests(unittest.TestCase):

    def get_token(self):
        pass

    def test_charge_request(self):

        # if no live_credentials module has been provided,
        # then we cannot run these tests
        try:
            from . import live_credentials
        except ImportError:
            self.skipTest("Live credentials not provided -- skipping tests")


        # try to get a token
        params = {'card_number': '4111111111111111',
                  'card_exp_month': '12',
                  'card_exp_year': '2020',
                  'card_cvv': '123',
                  'secure': False,
                  'gross_amount': 145000,
                  'client_key': live_credentials.SANDBOX_CLIENT_KEY,
                  }
        token_url = 'https://api.sandbox.veritrans.co.id/v2/token'
        resp = requests.get(token_url, params=params)

        if resp.status_code == codes.OK:
            token = resp.json()['token_id']
        else:
            self.fail("Failed retrieving token from server")

        # generate charge request
        expected = fixtures.CC_REQUEST
        cc_payment = payment_types.CreditCard(
            bank=expected['credit_card']['bank'],
            token_id=token)
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

        g = veritrans.VTDirect(live_credentials.SANDBOX_SERVER_KEY,
                               sandbox_mode=True)
        resp = g.submit_charge_request(charge_req)

        # self.fail(resp)
        # check the status
