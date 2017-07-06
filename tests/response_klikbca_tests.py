from unittest import TestCase

from veritranspay.response import KlikBCAChargeResponse


class KlikBCAChargeResponseTests_v0_9(TestCase):

    def setUp(self):
        # example response data from
        # --
        self.response_json = {
            "status_code": "201",
            "status_message": "Success, KlikBCA transaction is successful",
            "redirect_url": "https://www.klikbca.com",
            "transaction_id": "c0ba3583-5111-45a5-9f1c-84c9de7cb2f6",
            "order_id": "3176440",
            "gross_amount": "50000.00",
            "payment_type": "bca_klikbca",
            "transaction_time": "2016-06-19 15:53:25",
            "transaction_status": "pending",
            "approval_code": "tes01"
        }

        self.parsed_response = KlikBCAChargeResponse(**self.response_json)

    def test_status_code(self):
        self.assertEqual(201, self.parsed_response.status_code)

    def test_payment_type(self):
        self.assertEqual('bca_klikbca', self.parsed_response.payment_type)

