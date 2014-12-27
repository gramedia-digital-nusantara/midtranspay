from copy import deepcopy
import json
import unittest

from faker import Faker
from mock import MagicMock, patch

from veritranspay import request, validators, payment_types, veritrans
from veritranspay.response import response

from . import fixtures


fake = Faker()


class VTDirect_Init_Tests(unittest.TestCase):

    def setUp(self):
        # always set to None -- diff on things like arrays and hashes
        self.maxDiff = None
        # create ourselves a random server key for use in further tests
        self.server_key = "".join([fake.random_letter() for _ in range(45)])
        super(VTDirect_Init_Tests, self).setUp()

    def test_requires_server_key(self):
        ''' server_key should be a required init parameter. '''
        self.assertRaises(TypeError,
                          lambda: veritrans.VTDirect())

    def test_live_mode_is_default(self):
        '''
        When sandbox_mode is NOT explicitally set, VTDirect gateway should
        default to sandbox_mode=False.
        '''
        v = veritrans.VTDirect(server_key=self.server_key)
        self.assertFalse(v.sandbox_mode)

    def test_instance_attributes_set(self):
        '''
        Arguments passed to the constructor should persist themselves as
        instance attributes of the same name.
        '''
        v = veritrans.VTDirect(server_key=self.server_key,
                               sandbox_mode=False)
        self.assertEqual(v.server_key, self.server_key)
        self.assertFalse(v.sandbox_mode)

        v = veritrans.VTDirect(server_key=self.server_key,
                               sandbox_mode=True)
        self.assertEqual(v.server_key, self.server_key)
        self.assertTrue(v.sandbox_mode)

    def test_sanbox_mode_set_as_attribute(self):
        '''
        The value for 'sandbox_mode' passed to init should be persisted
        as an attribute with the same name.
        '''
        v = veritrans.VTDirect(server_key=self.server_key,
                               sandbox_mode=True)
        self.assertEqual(v.server_key, self.server_key)
        self.assertTrue(v.sandbox_mode)

    def test_sandbox_mode_expected_url(self):
        '''
        When sandbox_mode is True, we should receive the veritrans sandbox api
        URL back from the base_url property.
        '''
        v = veritrans.VTDirect(server_key=self.server_key,
                               sandbox_mode=True)
        self.assertEqual(v.base_url, veritrans.VTDirect.SANDBOX_API_URL)

    def test_live_mode_expected_url(self):
        '''
        When sandbox_mode is False, we should receive the veritrans live api
        URL back from the base_url property.
        '''
        v = veritrans.VTDirect(server_key=self.server_key,
                               sandbox_mode=False)
        self.assertEqual(v.base_url, veritrans.VTDirect.LIVE_API_URL)


class VTDirect_ChargeRequest_Tests(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.server_key = "".join([fake.random_letter() for _ in range(45)])

    def test_invalid_charge_request_raises_ValidationError(self):
        '''
        Make sure that if any of the sub-entities raise a ValidationError
        that it is bubbled out to calling code.
        '''
        gateway = veritrans.VTDirect(server_key=self.server_key)

        charge_req = MagicMock(spec=request.ChargeRequest)
        mock_validate = MagicMock(side_effect=validators.ValidationError)
        charge_req.attach_mock(mock_validate, 'validate_all')

        self.assertRaises(validators.ValidationError,
                          lambda: gateway.submit_charge_request(charge_req))

        self.assertEqual(mock_validate.call_count, 1)

    def test_submit_credit_card_charge(self):

        with patch('veritranspay.veritrans.requests.post') as mock_post:

            # create a fake key and request payload
            payload = {'charge_type': 'I am a little tea cup',
                       }

            gateway = veritrans.VTDirect(server_key=self.server_key)

            req = MagicMock()
            req.charge_type = MagicMock(spec=payment_types.CreditCard)
            req.attach_mock(MagicMock(return_value=payload),
                            'serialize')

            # mock the response data
            # so thta the JSON method returns a documented response
            # value
            mock_resp = MagicMock()
            mock_post.return_value = mock_resp
            mock_resp.attach_mock(
                MagicMock(return_value=fixtures.CC_CHARGE_RESPONSE_SUCCESS),
                'json')

            resp = gateway.submit_charge_request(req)

            # make sure requests library was called in the expected way.
            mock_post.assert_called_once_with(
                'https://api.veritrans.co.id/v2/charge',
                auth=(self.server_key, ''),
                headers={'content-type': 'application/json',
                         'accept': 'application/json'},
                data=json.dumps(payload))

            # did we get the expected response type?
            self.assertIsInstance(resp, response.CreditCardChargeResponse)

            # did it look like we expected
            expected_response_format = response.CreditCardChargeResponse(
                **fixtures.CC_CHARGE_RESPONSE_SUCCESS)

            # need to compare their dictionary formats
            self.assertEqual(expected_response_format.__dict__,
                             resp.__dict__)


class VTDirect_ApprovalRequest_UnitTests(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.server_key = "".join([fake.random_letter() for _ in range(45)])

    def test_invalid_approval_request_raises_ValidationError(self):
        gateway = veritrans.VTDirect(server_key=self.server_key)

        approval_req = MagicMock(spec=request.ApprovalRequest)
        mock_validate = MagicMock(side_effect=validators.ValidationError)
        approval_req.attach_mock(mock_validate, 'validate_all')

        self.assertRaises(validators.ValidationError,
                          lambda: gateway.submit_status_request(approval_req))

        self.assertEqual(mock_validate.call_count, 1)


class VTDirect_CancelRequest_UnitTests(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.server_key = "".join([fake.random_letter() for _ in range(45)])

    def test_invalid_cancel_request_raises_ValidationError(self):
        gateway = veritrans.VTDirect(server_key=self.server_key)

        cancel_req = MagicMock(spec=request.CancelRequest)
        mock_validate = MagicMock(side_effect=validators.ValidationError)
        cancel_req.attach_mock(mock_validate, 'validate_all')

        self.assertRaises(validators.ValidationError,
                          lambda: gateway.submit_status_request(cancel_req))

        self.assertEqual(mock_validate.call_count, 1)


class VTDirect_StatusRequest_UnitTests(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.server_key = "".join([fake.random_letter() for _ in range(45)])

    def test_invalid_status_request_raises_ValidationError(self):
        gateway = veritrans.VTDirect(server_key=self.server_key)

        status_req = MagicMock(spec=request.StatusRequest)
        mock_validate = MagicMock(side_effect=validators.ValidationError)
        status_req.attach_mock(mock_validate, 'validate_all')

        self.assertRaises(validators.ValidationError,
                          lambda: gateway.submit_status_request(status_req))

        self.assertEqual(mock_validate.call_count, 1)
