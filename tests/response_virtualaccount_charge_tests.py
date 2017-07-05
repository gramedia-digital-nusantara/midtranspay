from unittest import TestCase

from veritranspay.response.response import VirtualAccountBniChargeResponse, VirtualAccountPermataChargeResponse, \
    VirtualAccountBcaChargeResponse, VirtualAccountMandiriChargeResponse


class VirtualAccountPermataChargeResponseTests(TestCase):
    """
    https://api-docs.midtrans.com/#permata-virtual-account
    """
    def setUp(self):
        # example response data from
        # https://api-docs.midtrans.com/#permata-virtual-account
        self.response_json = {
            "status_code": "201",
            "status_message": "Success, PERMATA VA transaction is successful",
            "transaction_id": "6fd88567-62da-43ff-8fe6-5717e430ffc7",
            "order_id": "H17550",
            "gross_amount": "145000.00",
            "payment_type": "bank_transfer",
            "transaction_time": "2016-06-19 13:42:29",
            "transaction_status": "pending",
            "fraud_status": "accept",
            "permata_va_number": "8562000087926752"
        }

        self.parsed_response = VirtualAccountPermataChargeResponse(**self.response_json)

    def test_status_code(self):
        self.assertEqual(201, self.parsed_response.status_code)

    def test_payment_type(self):
        self.assertEqual('bank_transfer', self.parsed_response.payment_type)

    def test_payment_code(self):
        self.assertEqual('8562000087926752', self.parsed_response.permata_va_number)


class VirtualAccountBcaChargeResponseTests(TestCase):
    """
        https://api-docs.midtrans.com/#bca-virtual-account
    """
    def setUp(self):
        # example response data from
        # https://api-docs.midtrans.com/#bca-virtual-account
        self.response_json = {
            "status_code": "201",
            "status_message": "Success, Bank Transfer transaction is created",
            "transaction_id": "9aed5972-5b6a-401e-894b-a32c91ed1a3a",
            "order_id": "1466323342",
            "gross_amount": "20000.00",
            "payment_type": "bank_transfer",
            "transaction_time": "2016-06-19 15:02:22",
            "transaction_status": "pending",
            "va_numbers": [
                {
                    "bank": "bca",
                    "va_number": "91019021579"
                }
            ],
            "fraud_status": "accept"
        }

        self.parsed_response = VirtualAccountBcaChargeResponse(**self.response_json)

    def test_status_code(self):
        self.assertEqual(201, self.parsed_response.status_code)

    def test_payment_type(self):
        self.assertEqual('bank_transfer', self.parsed_response.payment_type)

    def test_payment_bank(self):
        self.assertEqual('bca', self.parsed_response.va_numbers[0]['bank'])

    def test_payment_vanumber(self):
        self.assertEqual('91019021579', self.parsed_response.va_numbers[0]['va_number'])


class VirtualAccountBniChargeResponseTests(TestCase):
    def setUp(self):
        # example response data from
        # https://api-docs.midtrans.com/#bni-virtual-account
        self.response_json = {
            "status_code": "201",
            "status_message": "Success, Bank Transfer transaction is created",
            "transaction_id": "9aed5972-5b6a-401e-894b-a32c91ed1a3a",
            "order_id": "1466323342",
            "gross_amount": "20000.00",
            "payment_type": "bank_transfer",
            "transaction_time": "2016-06-19 15:02:22",
            "transaction_status": "pending",
            "va_numbers": [
                {
                    "bank": "bni",
                    "va_number": "8578000000111111"
                }
            ],
            "fraud_status": "accept"
        }

        self.parsed_response = VirtualAccountBniChargeResponse(**self.response_json)

    def test_status_code(self):
        self.assertEqual(201, self.parsed_response.status_code)

    def test_payment_type(self):
        self.assertEqual('bank_transfer', self.parsed_response.payment_type)

    def test_payment_bank(self):
        self.assertEqual('Bni', self.parsed_response.bank)

    def test_payment_vabank(self):
        self.assertEqual('bni', self.parsed_response.va_numbers[0]['bank'])

    def test_payment_vanumber(self):
        self.assertEqual('8578000000111111', self.parsed_response.va_numbers[0]['va_number'])


class VirtualAccountMandiriChargeResponseTests(TestCase):
    def setUp(self):
        # example response data from
        # https://api-docs.midtrans.com/#mandiri-bill-payment
        self.response_json = {
            "status_code": "201",
            "status_message": "Success, Mandiri Bill transaction is successful",
            "transaction_id": "883af6a4-c1b4-4d39-9bd8-b148fcebe853",
            "order_id": "tes",
            "gross_amount": "1000.00",
            "payment_type": "echannel",
            "transaction_time": "2016-06-19 14:40:19",
            "transaction_status": "pending",
            "fraud_status": "accept",
            "bill_key": "990000000260",
            "biller_code": "70012"
        }

        self.parsed_response = VirtualAccountMandiriChargeResponse(**self.response_json)

    def test_status_code(self):
        self.assertEqual(201, self.parsed_response.status_code)

    def test_payment_type(self):
        self.assertEqual('echannel', self.parsed_response.payment_type)

    def test_payment_bank(self):
        self.assertEqual('990000000260', self.parsed_response.bill_key)

    def test_payment_vanumber(self):
        self.assertEqual('70012', self.parsed_response.biller_code)
