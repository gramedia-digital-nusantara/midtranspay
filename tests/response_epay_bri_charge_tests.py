from unittest import TestCase

from veritranspay.response.response import EpayBriChargeResponse


class EpayBriChargeResponseTests(TestCase):
    """
    https://api-docs.midtrans.com/#epay-bri
    """

    def setUp(self):
        # example response data from
        # https://api-docs.midtrans.com/#permata-virtual-account
        self.response_json = {
            "status_code": "201",
            "status_message": "Success, BRI E-Pay transaction is successful",
            "transaction_id": "f8635cd7-615d-4a6d-a806-c9ca4a56257e",
            "order_id": "2014111702",
            "redirect_url": "https://api.veritrans.co.id/v3/bri/epay/redirect/f8635cd7-615d-4a6d-a806-c9ca4a56257e",
            "gross_amount": "145000.00",
            "payment_type": "bri_epay",
            "transaction_time": "2016-06-19 16:00:05",
            "transaction_status": "pending",
            "fraud_status": "accept"
        }

        self.parsed_response = EpayBriChargeResponse(**self.response_json)

    def test_status_code(self):
        self.assertEqual(201, self.parsed_response.status_code)

    def test_payment_type(self):
        self.assertEqual('bri_epay', self.parsed_response.payment_type)

    def test_redirect_url(self):
        self.assertEqual('https://api.veritrans.co.id/v3/bri/epay/redirect/f8635cd7-615d-4a6d-a806-c9ca4a56257e', self.parsed_response.redirect_url)

