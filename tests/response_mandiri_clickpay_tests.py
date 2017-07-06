from unittest import TestCase

from veritranspay.response import MandiriChargeResponse


class MandiriChargeResponseTests_v0_9(TestCase):

    def setUp(self):
        # example response data from
        # http://api-docs.midtrans.com/#mandiri-clickpay
        self.response_json = {
            "status_code": "200",
            "status_message": "Success, Mandiri Clickpay transaction is successful",
            "transaction_id": "3bdddabe-a4ea-4233-81cc-09578178909f",
            "order_id": "100248319",
            "gross_amount": "156216.00",
            "payment_type": "mandiri_clickpay",
            "transaction_time": "2016-06-19 15:56:45",
            "transaction_status": "settlement",
            "fraud_status": "accept",
            "approval_code": "166JF5644001",
            "masked_card": "461699-9495"
        }

        self.parsed_response = MandiriChargeResponse(**self.response_json)

    def test_status_code(self):
        self.assertEqual(200, self.parsed_response.status_code)

    def test_payment_type(self):
        self.assertEqual('mandiri_clickpay', self.parsed_response.payment_type)

