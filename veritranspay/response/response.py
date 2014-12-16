from datetime import datetime
from veritranspay import mixins


class ChargeResponse(mixins.SerializableMixin):
    '''
    Encapsulates the response from Vertrans, returned after a ChargeRequest.
    '''
    def __init__(self,
                 payment_type,
                 status_code, status_message, order_id,
                 transaction_id, transaction_time, transaction_status,
                 fraud_status, masked_card, gross_amount,
                 bank=None, approval_code=None,
                 redirect_url=None, permata_va_number=None):
        '''
        :param bank: only when included in the request
        :param approval_code: only provided when successful.
        :param redirect_url: only for cimbs / epay bri
        :param permata_va_number: only for virtual account
        '''
        # absolutely everything in the response is string-encoded..
        # so we have to do a little massaging to get the format we want
        self.status_code = int(status_code)
        self.status_message = status_message
        self.transaction_id = transaction_id
        self.order_id = order_id
        self.payment_type = payment_type
        self.transaction_time = datetime.strptime(transaction_time,
                                                  '%Y-%m-%d %H:%M:%S')
        self.transaction_status = transaction_status
        self.fraud_status = fraud_status
        self.masked_card = masked_card
        self.bank = bank
        self.approval_code = approval_code
        self.redirect_url = redirect_url
        self.permata_va_number = permata_va_number
        # note: for some reason it's returning this with a fractional
        # portion, but currently only currency supported is IDR so int
        # .. plus we need to split off the fractional portion at the end
        # or python's int conversion will fail
        self.gross_amount = int(gross_amount.split('.')[0])

    def __repr__(self):
        return self.__str__()

