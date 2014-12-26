from veritranspay import mixins, helpers, payment_types


class ResponseBase(mixins.SerializableMixin):
    '''
    Base class for all responses from Veritrans.  The only two things
    we can be safely assured should be in every transaction are status_code
    and status_message.
    '''
    def __init__(self, status_code, status_message, *args, **kwargs):
        self.status_code = int(status_code)
        self.status_message = status_message

    def __repr__(self):
        return "<{klass}(code: {code}, message: {msg})>".format(
            klass=self.__class__.__name__,
            code=self.status_code,
            msg=self.status_message)


class ChargeResponseBase(ResponseBase):
    '''
    Encapsulates the response from Vertrans, returned after a ChargeRequest.
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

    def __init__(self, *args, **kwargs):
        super(CreditCardChargeResponse, self).__init__(*args, **kwargs)
        self.masked_card = kwargs.get('masked_card', None)
        self.bank = kwargs.get('bank', None)


class CimbsChargeResponse(ChargeResponseBase):

    def __init__(self, *args, **kwargs):
        super(CimbsChargeResponse, self).__init__(*args, **kwargs)
        self.redirect_url = kwargs.get('redirect_url', None)


class MandiriChargeResponse(ChargeResponseBase):

    def __init__(self, *args, **kwargs):
        super(MandiriChargeResponse, self).__init__(*args, **kwargs)
        self.masked_card = kwargs.get('masked_card', None)


class VirtualAccountChargeResponse(ChargeResponseBase):

    def __init__(self, *args, **kwargs):
        super(VirtualAccountChargeResponse, self).__init__(*args, **kwargs)
        self.permata_va_number = kwargs.get('permata_va_number', None)


def build_charge_response(request, *args, **kwargs):
    '''
    Builds a response appropriate for a given type of request.
    '''
    if type(request.charge_type) is payment_types.CreditCard:
        return CreditCardChargeResponse(*args, **kwargs)
    elif type(request.charge_type) is payment_types.CimbClicks:
        raise NotImplementedError("CimbClicks not yet supported.")
    elif type(request.charge_type) is payment_types.MandiriClickpay:
        raise NotImplementedError("MandiriClickpay not yet supported")
    else:
        return ChargeResponseBase(*args, **kwargs)


class StatusResponse(ResponseBase):
    '''
    Encapsulates information about the status of a single charge.
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
    Encapsulates response data for a request to cancel a single transaction.
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






