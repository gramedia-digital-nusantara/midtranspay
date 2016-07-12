from unittest import TestCase

from veritranspay.response import IndomaretChargeResponse


class IndomaretChargeResponseTests(TestCase):

    def setUp(self):
        # example response data from
        # http://docs.veritrans.co.id/en/vtdirect/integration_indomrt.html#response-transaction-indomrt
        self.response_json = {
            "status_code": "201",
            "status_message": "Success, CSTORE transaction is successful",
            "transaction_id": "ff05337c-6c94-4f70-8e81-35acd89b688e",
            "order_id": "201404141421",
            "payment_type": "cstore",
            "transaction_time": "2014-04-14 16:03:51",
            "transaction_status": "pending",
            "payment_code": "498112345234",
            "gross_amount": "145000.00"
        }

        self.parsed_response = IndomaretChargeResponse(**self.response_json)

    def test_status_code(self):
        self.assertEqual(201, self.parsed_response.status_code)

    def test_payment_type(self):
        self.assertEqual('cstore', self.parsed_response.payment_type)

    def test_payment_code(self):
        self.assertEqual('498112345234', self.parsed_response.payment_code)
