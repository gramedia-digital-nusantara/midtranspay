from copy import deepcopy
import json
import unittest

from faker import Faker
from mock import MagicMock, patch

from veritranspay import request, validators, payment_types, veritrans, \
    helpers
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
        '''
        Large test for submitting credit card charge.
        - Do we make our HTTP Request with the expected values
        - Do we get the correct response type back?
        - Does the response contain the data that it should?
        '''
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
                'https://api.midtrans.com/v2/charge',
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

    def test_submit_indomaret_charge(self):
        with patch('veritranspay.veritrans.requests.post') as mock_post:
            # create a fake key and request payload
            payload = {'charge_type': 'I am a little tea cup',
                       }

            gateway = veritrans.VTDirect(server_key=self.server_key)

            req = MagicMock()
            req.charge_type = MagicMock(spec=payment_types.Indomaret)
            req.attach_mock(MagicMock(return_value=payload), 'serialize')

            # mock the response data
            # so thta the JSON method returns a documented response
            # value
            mock_resp = MagicMock()
            mock_post.return_value = mock_resp
            mock_resp.attach_mock(
                MagicMock(return_value=fixtures.INDOMARET_CHARGE_RESPONSE_SUCCESS),
                'json')

            resp = gateway.submit_charge_request(req)

            # make sure requests library was called in the expected way.
            mock_post.assert_called_once_with(
                'https://api.midtrans.com/v2/charge',
                auth=(self.server_key, ''),
                headers={'content-type': 'application/json',
                         'accept': 'application/json'},
                data=json.dumps(payload))

            # did we get the expected response type?
            self.assertIsInstance(resp, response.IndomaretChargeResponse)

            # did it look like we expected
            expected_response_format = response.IndomaretChargeResponse(
                **fixtures.INDOMARET_CHARGE_RESPONSE_SUCCESS)

            # need to compare their dictionary formats
            self.assertEqual(expected_response_format.__dict__,
                             resp.__dict__)

    def test_submit_virtualaccountpermata_charge(self):
        with patch('veritranspay.veritrans.requests.post') as mock_post:
            # create a fake key and request payload
            payload = {'charge_type': 'I am a little tea cup',
                       }

            gateway = veritrans.VTDirect(server_key=self.server_key)

            req = MagicMock()
            req.charge_type = MagicMock(spec=payment_types.VirtualAccountPermata)
            req.attach_mock(MagicMock(return_value=payload), 'serialize')

            # mock the response data
            # so thta the JSON method returns a documented response
            # value
            mock_resp = MagicMock()
            mock_post.return_value = mock_resp
            mock_resp.attach_mock(
                MagicMock(return_value=fixtures.VIRTUALACCOUNTPERMATA_CHARGE_RESPONSE_SUCCESS),
                'json')

            resp = gateway.submit_charge_request(req)

            # make sure requests library was called in the expected way.
            mock_post.assert_called_once_with(
                'https://api.midtrans.com/v2/charge',
                auth=(self.server_key, ''),
                headers={'content-type': 'application/json',
                         'accept': 'application/json'},
                data=json.dumps(payload))

            # did we get the expected response type?
            self.assertIsInstance(resp, response.VirtualAccountPermataChargeResponse)

            # did it look like we expected
            expected_response_format = response.VirtualAccountPermataChargeResponse(
                **fixtures.VIRTUALACCOUNTPERMATA_CHARGE_RESPONSE_SUCCESS)

            # need to compare their dictionary formats
            self.assertEqual(expected_response_format.__dict__,
                             resp.__dict__)

    def test_submit_virtualaccountmandiri_charge(self):
        with patch('veritranspay.veritrans.requests.post') as mock_post:
            # create a fake key and request payload
            payload = {'charge_type': 'I am a little tea cup',
                       }

            gateway = veritrans.VTDirect(server_key=self.server_key)

            req = MagicMock()
            req.charge_type = MagicMock(spec=payment_types.VirtualAccountMandiri)
            req.attach_mock(MagicMock(return_value=payload), 'serialize')

            # mock the response data
            # so thta the JSON method returns a documented response
            # value
            mock_resp = MagicMock()
            mock_post.return_value = mock_resp
            mock_resp.attach_mock(
                MagicMock(return_value=fixtures.VIRTUALACCOUNTMANDIRI_CHARGE_RESPONSE_SUCCESS),
                'json')

            resp = gateway.submit_charge_request(req)

            # make sure requests library was called in the expected way.
            mock_post.assert_called_once_with(
                'https://api.midtrans.com/v2/charge',
                auth=(self.server_key, ''),
                headers={'content-type': 'application/json',
                         'accept': 'application/json'},
                data=json.dumps(payload))

            # did we get the expected response type?
            self.assertIsInstance(resp, response.VirtualAccountMandiriChargeResponse)

            # did it look like we expected
            expected_response_format = response.VirtualAccountMandiriChargeResponse(
                **fixtures.VIRTUALACCOUNTMANDIRI_CHARGE_RESPONSE_SUCCESS)

            # need to compare their dictionary formats
            self.assertEqual(expected_response_format.__dict__,
                             resp.__dict__)

    def test_submit_briepay_charge(self):
        with patch('veritranspay.veritrans.requests.post') as mock_post:
            # create a fake key and request payload
            payload = {'charge_type': 'I am a little tea cup',
                       }

            gateway = veritrans.VTDirect(server_key=self.server_key)

            req = MagicMock()
            req.charge_type = MagicMock(spec=payment_types.BriEpay)
            req.attach_mock(MagicMock(return_value=payload), 'serialize')

            # mock the response data
            # so that the JSON method returns a documented response
            # value
            mock_resp = MagicMock()
            mock_post.return_value = mock_resp
            mock_resp.attach_mock(
                MagicMock(return_value=fixtures.BRIEPAY_CHARGE_RESPONSE_SUCCESS),
                'json')

            resp = gateway.submit_charge_request(req)

            # make sure requests library was called in the expected way.
            mock_post.assert_called_once_with(
                'https://api.midtrans.com/v2/charge',
                auth=(self.server_key, ''),
                headers={'content-type': 'application/json',
                         'accept': 'application/json'},
                data=json.dumps(payload))

            # did we get the expected response type?
            self.assertIsInstance(resp, response.EpayBriChargeResponse)

            # did it look like we expected
            expected_response_format = response.EpayBriChargeResponse(
                **fixtures.BRIEPAY_CHARGE_RESPONSE_SUCCESS)

            # need to compare their dictionary formats
            self.assertEqual(expected_response_format.__dict__,
                             resp.__dict__)


class VTDirect_ApprovalRequest_UnitTests(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.server_key = "".join([fake.random_letter() for _ in range(45)])

    def test_invalid_approval_request_raises_ValidationError(self):
        '''
        Validation error should be bubbled-up to the calling client code.
        '''
        gateway = veritrans.VTDirect(server_key=self.server_key)

        approval_req = MagicMock(spec=request.ApprovalRequest)
        mock_validate = MagicMock(side_effect=validators.ValidationError)
        approval_req.attach_mock(mock_validate, 'validate_all')

        self.assertRaises(validators.ValidationError,
                          lambda: gateway.submit_status_request(approval_req))

        self.assertEqual(mock_validate.call_count, 1)

    def test_submit_approval_request(self):
        '''
        Large test:
        - Do we make our HTTP request with the expected values?
        - Do we get back the proper response type
        - Does the response contain the data we think it should?
        '''
        with patch('veritranspay.veritrans.requests.post') as mock_post:

            order_id = ''.join([fake.random_letter() for _ in range(25)])

            # mock out our approval request
            req = MagicMock(spec=request.ApprovalRequest)
            req.order_id = order_id
            # req.attach_mock(MagicMock(return_value=order_id), 'order_id')
            req.attach_mock(MagicMock(return_value=None), 'validate_all')

            # mock out our HTTP post
            mock_resp = MagicMock()
            mock_resp.attach_mock(
                MagicMock(return_value=fixtures.APPROVE_RESPONSE),
                'json')
            mock_post.return_value = mock_resp

            # get a response from the gateway
            gateway = veritrans.VTDirect(self.server_key)
            resp = gateway.submit_approval_request(req)

            # did we make our HTTP request properly?
            mock_post.assert_called_once_with(
                'https://api.midtrans.com/v2/'
                '{order_id}/approve'.format(order_id=order_id),
                auth=(self.server_key, ''),
                headers={'accept': 'application/json'}
            )

            # was it the correct type?
            self.assertIsInstance(resp, response.ApproveResponse)

            # last, take our expected return values and do a little
            # massaging out to account for modifications performed
            # by response object
            exp = deepcopy(fixtures.APPROVE_RESPONSE)
            exp['status_code'] = int(exp['status_code'])
            exp['transaction_time'] = \
                helpers.parse_veritrans_datetime(exp['transaction_time'])
            exp['gross_amount'] = \
                helpers.parse_veritrans_amount(exp['gross_amount'])

            # does it have our expected attributes?
            self.assertEqual(resp.status_code,
                             int(exp['status_code']))
            self.assertEqual(resp.status_message, exp['status_message'])
            self.assertEqual(resp.transaction_id, exp['transaction_id'])
            self.assertEqual(resp.masked_card, exp['masked_card'])
            self.assertEqual(resp.order_id, exp['order_id'])
            self.assertEqual(resp.payment_type, exp['payment_type'])
            self.assertEqual(resp.transaction_time, exp['transaction_time'])
            self.assertEqual(resp.transaction_status,
                             exp['transaction_status'])
            self.assertEqual(resp.fraud_status, exp['fraud_status'])
            self.assertEqual(resp.approval_code, exp['approval_code'])
            self.assertEqual(resp.bank, exp['bank'])
            self.assertEqual(resp.gross_amount, exp['gross_amount'])


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

    def test_submit_cancel_request(self):
        '''
        Large test:
        - Do we make our HTTP request with the expected values?
        - Do we get back the proper response type
        - Does the response contain the data we think it should?
        '''
        with patch('veritranspay.veritrans.requests.post') as mock_post:

            order_id = ''.join([fake.random_letter() for _ in range(25)])

            # mock out our approval request
            req = MagicMock(spec=request.CancelRequest)
            req.order_id = order_id
            # req.attach_mock(MagicMock(return_value=order_id), 'order_id')
            req.attach_mock(MagicMock(return_value=None), 'validate_all')

            # mock out our HTTP post
            mock_resp = MagicMock()
            mock_resp.attach_mock(
                MagicMock(return_value=fixtures.CANCEL_RESPONSE),
                'json')
            mock_post.return_value = mock_resp

            # get a response from the gateway
            gateway = veritrans.VTDirect(self.server_key)
            resp = gateway.submit_cancel_request(req)

            # did we make our HTTP request properly?
            mock_post.assert_called_once_with(
                'https://api.midtrans.com/v2/'
                '{order_id}/cancel'.format(order_id=order_id),
                auth=(self.server_key, ''),
                headers={'accept': 'application/json'}
            )

            # was it the correct type?
            self.assertIsInstance(resp, response.CancelResponse)

            # last, take our expected return values and do a little
            # massaging out to account for modifications performed
            # by response object
            exp = deepcopy(fixtures.CANCEL_RESPONSE)
            exp['status_code'] = int(exp['status_code'])
            exp['transaction_time'] = \
                helpers.parse_veritrans_datetime(exp['transaction_time'])
            exp['gross_amount'] = \
                helpers.parse_veritrans_amount(exp['gross_amount'])

            # does it have our expected attributes?
            self.assertEqual(resp.status_code,
                             int(exp['status_code']))
            self.assertEqual(resp.status_message, exp['status_message'])
            self.assertEqual(resp.transaction_id, exp['transaction_id'])
            self.assertEqual(resp.masked_card, exp['masked_card'])
            self.assertEqual(resp.order_id, exp['order_id'])
            self.assertEqual(resp.payment_type, exp['payment_type'])
            self.assertEqual(resp.transaction_time, exp['transaction_time'])
            self.assertEqual(resp.transaction_status,
                             exp['transaction_status'])
            self.assertEqual(resp.fraud_status, exp['fraud_status'])
            self.assertEqual(resp.bank, exp['bank'])
            self.assertEqual(resp.gross_amount, exp['gross_amount'])


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

    def test_submit_status_request(self):
        '''
        Large test:
        - Do we make our HTTP request with the expected values?
        - Do we get back the proper response type
        - Does the response contain the data we think it should?
        '''
        with patch('veritranspay.veritrans.requests.post') as mock_post:

            order_id = ''.join([fake.random_letter() for _ in range(25)])

            # mock out our approval request
            req = MagicMock(spec=request.ApprovalRequest)
            req.order_id = order_id
            # req.attach_mock(MagicMock(return_value=order_id), 'order_id')
            req.attach_mock(MagicMock(return_value=None), 'validate_all')

            # mock out our HTTP post
            mock_resp = MagicMock()
            mock_resp.attach_mock(
                MagicMock(return_value=fixtures.STATUS_RESPONSE),
                'json')
            mock_post.return_value = mock_resp

            # get a response from the gateway
            gateway = veritrans.VTDirect(self.server_key)
            resp = gateway.submit_approval_request(req)

            # did we make our HTTP request properly?
            mock_post.assert_called_once_with(
                'https://api.midtrans.com/v2/'
                '{order_id}/approve'.format(order_id=order_id),
                auth=(self.server_key, ''),
                headers={'accept': 'application/json'}
            )

            # was it the correct type?
            self.assertIsInstance(resp, response.ApproveResponse)

            # last, take our expected return values and do a little
            # massaging out to account for modifications performed
            # by response object
            exp = deepcopy(fixtures.STATUS_RESPONSE)
            exp['status_code'] = int(exp['status_code'])
            exp['transaction_time'] = \
                helpers.parse_veritrans_datetime(exp['transaction_time'])
            exp['gross_amount'] = \
                helpers.parse_veritrans_amount(exp['gross_amount'])

            # does it have our expected attributes?
            self.assertEqual(resp.status_code,
                             int(exp['status_code']))
            self.assertEqual(resp.status_message, exp['status_message'])
            self.assertEqual(resp.transaction_id, exp['transaction_id'])
            self.assertEqual(resp.masked_card, exp['masked_card'])
            self.assertEqual(resp.order_id, exp['order_id'])
            self.assertEqual(resp.payment_type, exp['payment_type'])
            self.assertEqual(resp.transaction_time, exp['transaction_time'])
            self.assertEqual(resp.transaction_status,
                             exp['transaction_status'])
            self.assertEqual(resp.fraud_status, exp['fraud_status'])
            self.assertEqual(resp.approval_code, exp['approval_code'])
            self.assertEqual(resp.signature_key, exp['signature_key'])
            self.assertEqual(resp.bank, exp['bank'])
            self.assertEqual(resp.gross_amount, exp['gross_amount'])
