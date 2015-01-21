'''
Response objects are generated by a gateway after data is sent back from
Veritrans about a request.  Response formats can vary depending on the
type of error encountered from Veritrans, so the only two parameters
that are required for ALL responses are status_code, and status_message.
The rest are all purely optional (though unexpected parameters will be
ignored).

To see the expected attributes for a given type of request, check
the documentation at:

- http://docs.veritrans.co.id/sandbox/other_commands.html
- http://docs.veritrans.co.id/sandbox/charge.html
'''
from veritranspay import mixins, helpers, payment_types


class ResponseBase(mixins.SerializableMixin):
    '''
    Base class for all responses from Veritrans.  The only two things
    we can be safely assured should be in every transaction are status_code
    and status_message.
    '''
    def __init__(self, status_code, status_message, *args, **kwargs):
        '''
        :param status_code: Transaction status code supplied by Veritrans.
        :type status_code: :py:class:`str`
        :param status_message: Human-readable status message.
        :type status_message: :py:class:`str`
        '''
        self.status_code = int(status_code)
        self.status_message = status_message

    def __repr__(self):
        return "<{klass}(code: {code}, message: {msg})>".format(
            klass=self.__class__.__name__,
            code=self.status_code,
            msg=self.status_message)


class ChargeResponseBase(ResponseBase):
    '''
    Encapsulates the response from Vertrans, returned after a
    :py:class:`veritranspay.request.ChargeRequest`.
    '''
    def __init__(self, *args, **kwargs):
        super(ChargeResponseBase, self).__init__(*args, **kwargs)
        self.transaction_id = kwargs.get('transaction_id', None)
        self.order_id = kwargs.get('order_id', None)
        self.payment_type = kwargs.get('payment_type', None)
        self.transaction_time = \
            helpers.parse_veritrans_datetime(
                kwargs.get('transaction_time', None))
        self.transaction_status = kwargs.get('transaction_status', None)
        self.fraud_status = kwargs.get('fraud_status', None)
        self.approval_code = kwargs.get('approval_code', None)
        self.gross_amount = \
            helpers.parse_veritrans_amount(
                kwargs.get('gross_amount', None))


class CreditCardChargeResponse(ChargeResponseBase):
    '''
    Response from Veritrans, returned after a
    :py:class:`veritrans.request.ChargeRequest` with a charge type of
    :py:class:`veritrans.payment_types.CreditCard`.
    '''
    def __init__(self, *args, **kwargs):
        super(CreditCardChargeResponse, self).__init__(*args, **kwargs)
        self.masked_card = kwargs.get('masked_card', None)
        self.bank = kwargs.get('bank', None)
        self.masked_card = kwargs.get('masked_card', None)
        self.saved_token_id = kwargs.get('saved_token_id')
        self.saved_token_id_expired_at = helpers.parse_veritrans_datetime(
            kwargs.get("saved_token_id_expired_at", None))

class CimbsChargeResponse(ChargeResponseBase):
    # not implemented -- not documented
    def __init__(self, *args, **kwargs):
        super(CimbsChargeResponse, self).__init__(*args, **kwargs)
        self.redirect_url = kwargs.get('redirect_url', None)


class MandiriChargeResponse(ChargeResponseBase):
    # not implemented -- not documented
    def __init__(self, *args, **kwargs):
        super(MandiriChargeResponse, self).__init__(*args, **kwargs)
        self.masked_card = kwargs.get('masked_card', None)


class VirtualAccountChargeResponse(ChargeResponseBase):
    # not implemented -- not documented
    def __init__(self, *args, **kwargs):
        super(VirtualAccountChargeResponse, self).__init__(*args, **kwargs)
        self.permata_va_number = kwargs.get('permata_va_number', None)


def build_charge_response(request, *args, **kwargs):
    '''
    Builds a response appropriate for a given type of request.

    :param request: The request that was submitted to Veritrans.
        The charge_type is used to determine the appropriate
        response type to build.
    :type request: :py:class:`veritranspay.request.ChargeRequest`
    '''
    if isinstance(request.charge_type, payment_types.CreditCard):
        return CreditCardChargeResponse(*args, **kwargs)
    elif isinstance(request.charge_type, payment_types.CimbClicks):
        raise NotImplementedError("CimbClicks not yet supported.")
    elif isinstance(request.charge_type, payment_types.MandiriClickpay):
        raise NotImplementedError("MandiriClickpay not yet supported")
    else:
        return ChargeResponseBase(*args, **kwargs)


class StatusResponse(ResponseBase):
    '''
    Encapsulates information about the status of a single charge.
    Returned from Veritrans after submitting a
    :py:class:`veritranspay.request.StatusRequest`
    '''
    def __init__(self, *args, **kwargs):
        super(StatusResponse, self).__init__(*args, **kwargs)
        self.transaction_id = kwargs.get('transaction_id', None)
        self.masked_card = kwargs.get('masked_card', None)
        self.order_id = kwargs.get('order_id', None)
        self.payment_type = kwargs.get('payment_type', None)
        self.transaction_time = \
            helpers.parse_veritrans_datetime(
                kwargs.get('transaction_time', None))
        self.transaction_status = kwargs.get('transaction_status', None)
        self.fraud_status = kwargs.get('fraud_status', None)
        self.approval_code = kwargs.get('approval_code', None)
        self.signature_key = kwargs.get('signature_key', None)
        self.bank = kwargs.get('bank', None)
        self.gross_amount = \
            helpers.parse_veritrans_amount(
                kwargs.get('gross_amount', None))


class CancelResponse(ResponseBase):
    '''
    Data returned from Veritrans after submitting a
    :py:class:`veritranspay.request.CancelRequest`.
    '''
    def __init__(self, *args, **kwargs):
        super(CancelResponse, self).__init__(*args, **kwargs)
        self.transaction_id = kwargs.get('transaction_id', None)
        self.masked_card = kwargs.get('masked_card', None)
        self.order_id = kwargs.get('order_id', None)
        self.payment_type = kwargs.get('payment_type', None)
        self.transaction_time = \
            helpers.parse_veritrans_datetime(
                kwargs.get('transaction_time', None))
        self.transaction_status = kwargs.get('transaction_status', None)
        self.fraud_status = kwargs.get('fraud_status', None)
        self.approval_code = kwargs.get('approval_code', None)
        self.signature_key = kwargs.get('signature_key', None)
        self.bank = kwargs.get('bank', None)
        self.gross_amount = \
            helpers.parse_veritrans_amount(
                kwargs.get('gross_amount', None))


class ApproveResponse(ResponseBase):
    '''
    Data returned from Veritrans after submitting a
    :py:class:`veritranspay.request.ApprovalRequest`
    '''
    def __init__(self, *args, **kwargs):
        super(ApproveResponse, self).__init__(*args, **kwargs)
        self.transaction_id = kwargs.get('transaction_id', None)
        self.masked_card = kwargs.get('masked_card', None)
        self.order_id = kwargs.get('order_id', None)
        self.payment_type = kwargs.get('payment_type', None)
        self.transaction_time = \
            helpers.parse_veritrans_datetime(
                kwargs.get('transaction_time', None))
        self.transaction_status = kwargs.get('transaction_status', None)
        self.fraud_status = kwargs.get('fraud_status', None)
        self.approval_code = kwargs.get('approval_code', None)
        self.signature_key = kwargs.get('signature_key', None)
        self.bank = kwargs.get('bank', None)
        self.gross_amount = \
            helpers.parse_veritrans_amount(
                kwargs.get('gross_amount', None))
