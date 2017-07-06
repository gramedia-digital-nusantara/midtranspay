from unittest import TestCase

from midtranspay.response import CimbsChargeResponse


class CimbsChargeResponseTests_v0_9(TestCase):

    def setUp(self):
        # example response data from
        # http://api-docs.midtrans.com/#cimb-clicks
        self.response_json = {
            "status_code": "201",
            "status_message": "Success, CIMB Clicks transaction is successful",
            "redirect_url": "https://api.midtrans.com/cimb-clicks/request?id=226f042f-020e-4829-8bd7-2de64b8673ce",
            "transaction_id": "226f042f-020e-4829-8bd7-2de64b8673ce",
            "order_id": "1000156414164125",
            "gross_amount": "392127.00",
            "payment_type": "cimb_clicks",
            "transaction_time": "2016-06-19 16:41:25",
            "transaction_status": "pending"
        }

        self.parsed_response = CimbsChargeResponse(**self.response_json)

    def test_status_code(self):
        self.assertEqual(201, self.parsed_response.status_code)

    def test_payment_type(self):
        self.assertEqual('cimb_clicks', self.parsed_response.payment_type)

