from unittest import TestCase

from veritranspay.response import BinResponse


class BinsRequestResponseTests(TestCase):

    def setUp(self):
        # example response data from
        # --
        self.response_json = {
            "data": {
                "country_name": "Indonesia",
                "country_code": "id",
                "brand": "visa",
                "bin_type": "credit",
                "bin_class": "gold",
                "bin": "455633",
                "bank_code": "bca",
                "bank": "bank central asia"
            }
        }

        self.parsed_response = BinResponse(status_code=200, status_message='',**self.response_json)

    def test_status_code(self):
        self.assertEqual(200, self.parsed_response.status_code)

    def test_response_data(self):
        self.assertEqual(self.parsed_response.serialize().get('data'), self.response_json.get('data'))

