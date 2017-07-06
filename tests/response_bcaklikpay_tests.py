from unittest import TestCase

from midtranspay.response import BCAKlikPayChargeResponse


class BCAKlikPayChargeResponseTests_v0_9(TestCase):

    def setUp(self):
        # example response data from
        # http://api-docs.midtrans.com/#bca-klikpay
        self.response_json = {
              "status_code": "201",
              "status_message": "OK, BCA KlikPay transaction is successful",
              "transaction_id": "ada84cd9-2233-4c67-877a-01884eece45e",
              "order_id": "orderid-01",
              "redirect_url": "https://api.sandbox.midtrans.co.id/v3/bca/klikpay/redirect/ada84cd9-2233-4c67-877a-01884eece45e",
              "gross_amount": "11000.00",
              "payment_type": "bca_klikpay",
              "transaction_time": "2016-06-19 15:42:36",
              "transaction_status": "pending",
              "fraud_status": "accept"
        }

        self.parsed_response = BCAKlikPayChargeResponse(**self.response_json)

    def test_status_code(self):
        self.assertEqual(201, self.parsed_response.status_code)

    def test_payment_type(self):
        self.assertEqual('bca_klikpay', self.parsed_response.payment_type)

