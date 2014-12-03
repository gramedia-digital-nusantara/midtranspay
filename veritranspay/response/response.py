from datetime import datetime
from veritranspay import mixins


class Response(mixins.SerializableMixin):

    def __init__(self, status_code, status_message, transaction_id, order_id,
                 payment_type, transaction_time, transaction_status,
                 fraud_status, masked_card, bank, approval_code, gross_amount):

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
        # note: for some reason it's returning this with a fractional
        # portion, but currently only currency supported is IDR so int
        self.gross_amount = int(gross_amount)



