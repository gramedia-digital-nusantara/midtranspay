from unittest import TestCase

from veritranspay.response.response import GoPayChargeResponse


class GoPayChargeResponseTests(TestCase):
    """
    https://api-docs.midtrans.com/#epay-bri
    """

    def setUp(self):
        # example response data from
        # https://api-docs.midtrans.com/#go-pay
        self.actions = [{
            "name": "generate-qr-code",
            "method": "GET",
            "url": "https://api.midtrans.com/v2/gopay/e48447d1-cfa9-4b02-b163-2e915d4417ac/qr-code"
        },
            {
                "name": "deeplink-redirect",
                "method": "GET",
                "url": "gojek://gopay/merchanttransfer?tref=1509110800474199656LMVO&amount=10000&activity=GP:RR"
            },
            {
                "name": "get-status",
                "method": "GET",
                "url": "https://api.midtrans.com/v2/e48447d1-cfa9-4b02-b163-2e915d4417ac/status"
            },
            {
                "name": "cancel",
                "method": "POST",
                "url": "https://api.midtrans.com/v2/e48447d1-cfa9-4b02-b163-2e915d4417ac/cancel",
                "fields": []
            }
        ]
        self.response_json = {
            "status_code": "201",
            "status_message": "GO-PAY billing created",
            "transaction_id": "e48447d1-cfa9-4b02-b163-2e915d4417ac",
            "order_id": "SAMPLE-ORDER-ID-01",
            "gross_amount": "10000.00",
            "payment_type": "gopay",
            "transaction_time": "2017-10-04 12:00:00",
            "transaction_status": "pending",
            "actions": [{
                "name": "generate-qr-code",
                "method": "GET",
                "url": "https://api.midtrans.com/v2/gopay/e48447d1-cfa9-4b02-b163-2e915d4417ac/qr-code"
            },
                {
                    "name": "deeplink-redirect",
                    "method": "GET",
                    "url": "gojek://gopay/merchanttransfer?tref=1509110800474199656LMVO&amount=10000&activity=GP:RR"
                },
                {
                    "name": "get-status",
                    "method": "GET",
                    "url": "https://api.midtrans.com/v2/e48447d1-cfa9-4b02-b163-2e915d4417ac/status"
                },
                {
                    "name": "cancel",
                    "method": "POST",
                    "url": "https://api.midtrans.com/v2/e48447d1-cfa9-4b02-b163-2e915d4417ac/cancel",
                    "fields": []
                }
            ],
            "channel_response_code": "200",
            "channel_response_message": "Success",
            "currency": "IDR"
        }

        self.parsed_response = GoPayChargeResponse(**self.response_json)

    def test_status_code(self):
        self.assertEqual(201, self.parsed_response.status_code)

    def test_payment_type(self):
        self.assertEqual('gopay', self.parsed_response.payment_type)

    def test_redirect_url(self):
        self.assertEqual(self.actions, self.parsed_response.actions)

