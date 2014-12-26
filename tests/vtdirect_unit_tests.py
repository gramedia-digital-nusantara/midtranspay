import unittest

from faker import Faker
from mock import MagicMock

from veritranspay import request, validators, payment_types
from veritranspay.veritrans import VTDirect

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
                          lambda: VTDirect())

    def test_live_mode_is_default(self):
        '''
        When sandbox_mode is NOT explicitally set, VTDirect gateway should
        default to sandbox_mode=False.
        '''
        v = VTDirect(server_key=self.server_key)
        self.assertFalse(v.sandbox_mode)

    def test_instance_attributes_set(self):
        '''
        Arguments passed to the constructor should persist themselves as
        instance attributes of the same name.
        '''
        v = VTDirect(server_key=self.server_key,
                     sandbox_mode=False)
        self.assertEqual(v.server_key, self.server_key)
        self.assertFalse(v.sandbox_mode)

        v = VTDirect(server_key=self.server_key,
                     sandbox_mode=True)
        self.assertEqual(v.server_key, self.server_key)
        self.assertTrue(v.sandbox_mode)

    def test_sanbox_mode_set_as_attribute(self):
        '''
        The value for 'sandbox_mode' passed to init should be persisted
        as an attribute with the same name.
        '''
        v = VTDirect(server_key=self.server_key,
                     sandbox_mode=True)
        self.assertEqual(v.server_key, self.server_key)
        self.assertTrue(v.sandbox_mode)

    def test_sandbox_mode_expected_url(self):
        '''
        When sandbox_mode is True, we should receive the veritrans sandbox api
        URL back from the base_url property.
        '''
        v = VTDirect(server_key=self.server_key,
                     sandbox_mode=True)
        self.assertEqual(v.base_url, VTDirect.SANDBOX_API_URL)

    def test_live_mode_expected_url(self):
        '''
        When sandbox_mode is False, we should receive the veritrans live api
        URL back from the base_url property.
        '''
        v = VTDirect(server_key=self.server_key,
                     sandbox_mode=False)
        self.assertEqual(v.base_url, VTDirect.LIVE_API_URL)

    def test_stringifies_as_expected(self):
        self.skipTest("")

    def test_invalid_charge_request_raises_ValidationError(self):
        '''
        Make sure that if any of the sub-entities raise a ValidationError
        that it is bubbled out to calling code.
        '''
        gateway = VTDirect(server_key=self.server_key)

        charge_req = MagicMock(spec=request.ChargeRequest)
        mock_validate = MagicMock(side_effect=validators.ValidationError)
        charge_req.attach_mock(mock_validate, 'validate_all')

        self.assertRaises(validators.ValidationError,
                          lambda: gateway.submit_charge_request(charge_req))

        self.assertEqual(mock_validate.call_count, 1)

    def test_invalid_status_request_raises_ValidationError(self):
        gateway = VTDirect(server_key=self.server_key)

        status_req = MagicMock(spec=request.StatusRequest)
        mock_validate = MagicMock(side_effect=validators.ValidationError)
        status_req.attach_mock(mock_validate, 'validate_all')

        self.assertRaises(validators.ValidationError,
                          lambda: gateway.submit_status_request(status_req))

        self.assertEqual(mock_validate.call_count, 1)

    def test_invalid_cancel_request_raises_ValidationError(self):
        gateway = VTDirect(server_key=self.server_key)

        cancel_req = MagicMock(spec=request.CancelRequest)
        mock_validate = MagicMock(side_effect=validators.ValidationError)
        cancel_req.attach_mock(mock_validate, 'validate_all')

        self.assertRaises(validators.ValidationError,
                          lambda: gateway.submit_status_request(cancel_req))

        self.assertEqual(mock_validate.call_count, 1)

    def test_invalid_approval_request_raises_ValidationError(self):
        gateway = VTDirect(server_key=self.server_key)

        approval_req = MagicMock(spec=request.ApprovalRequest)
        mock_validate = MagicMock(side_effect=validators.ValidationError)
        approval_req.attach_mock(mock_validate, 'validate_all')

        self.assertRaises(validators.ValidationError,
                          lambda: gateway.submit_status_request(approval_req))

        self.assertEqual(mock_validate.call_count, 1)

    def test_cancel_request_calls_expected_url(self):
        self.skipTest("Not Implemented")

    def test_cancel_request_has_expected_accept_headers(self):
        self.skipTest("Not Implemented")

    def test_cancel_request_has_expected_auth_header(self):
        self.skipTest("Not Implemented")

    def test_cancel_request_returns_expected_object(self):
        self.skipTest("Not Implemented")

    def test_approval_request_calls_expected_url(self):
        self.skipTest("Not Implemented")

    def test_approval_request_has_expected_accept_headers(self):
        self.skipTest("Not Implemented")

    def test_approval_request_has_expected_auth_headers(self):
        self.skipTest("Not Implemented")

    def test_approval_request_returns_expected_object(self):
        self.skipTest("Not Implemented")

    def test_submit_request_calls_expected_url(self):
        self.skipTest("Not Implemented")

    def test_submit_request_has_expected_accept_headers(self):
        self.skipTest("Not Implemented")

    def test_submit_request_has_expected_auth_headers(self):
        self.skipTest("Not Implemented")

    def test_submit_request_returns_expected_object(self):
        self.skipTest("Not Implemented")

    def test_cc_serialization(self):
        ''' Given a complete request format--make sure that our ChargeRequest
        is serializing out the same format.
        '''
        # TODO: This belongs on ChargeRequest unit tests!
        expected = fixtures.CC_REQUEST

        cc_payment = payment_types.CreditCard(
            bank=expected['credit_card']['bank'],
            token_id=expected['credit_card']['token_id'])
        trans_details = request.TransactionDetails(
            order_id=expected['transaction_details']['order_id'],
            gross_amount=expected['transaction_details']['gross_amount'])
        cust_details = request.CustomerDetails(
            first_name=expected['customer_details']['first_name'],
            last_name=expected['customer_details']['last_name'],
            email=expected['customer_details']['email'],
            phone=expected['customer_details']['phone'],
            billing_address=request.Address(
                **expected['customer_details']['billing_address']),
            shipping_address=request.Address(
                **expected['customer_details']['shipping_address'])
            )
        item_details = [request.ItemDetails(item_id=item['id'],
                                            price=item['price'],
                                            quantity=item['quantity'],
                                            name=item['name'])
                        for item
                        in expected['item_details']]

        charge_req = request.ChargeRequest(charge_type=cc_payment,
                                           transaction_details=trans_details,
                                           customer_details=cust_details,
                                           item_details=item_details)

        actual = charge_req.serialize()

        self.assertEqual(actual, expected)


class VTDirect_CommandTests_Base(object):
    # request.validate_all called
    # validationError bubbles up
    # has expected headers
    # calls expected URL sandbox
    # calls expected URL live
    # expected auth parameters
    # raises urllib3 errors -- look into this
    # fails if malformed json
    # returns expected object for request success
    pass

class VTDirect_ChargeRequest_Tests(VTDirect_CommandTests_Base):
    # returns expected object
    # returns expected object for test request failure -- need to figure out
    #     what a failure response actually looks like here!
    pass

class VTDirect_OtherCommandTests_Base(VTDirect_CommandTests_Base):
    pass


class VTDirect_ApprovalRequest_UnitTests(VTDirect_OtherCommandTests_Base):
    pass


class VTDirect_CancelRequest_UnitTests(VTDirect_OtherCommandTests_Base):
    pass


class VTDirect_StatusRequest_UnitTests(VTDirect_OtherCommandTests_Base):
    pass
