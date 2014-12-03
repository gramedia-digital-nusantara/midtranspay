
class PaymentTypeBase(object):

    def serialize(self):
        return {"payment_type": self.PAYMENT_TYPE_KEY,
                self.PAYMENT_TYPE_KEY: {},
                }


class CreditCard(PaymentTypeBase):
    # http://docs.veritranspay.co.id/sandbox/charge.html#vtdirect-cc
    PAYMENT_TYPE_KEY = 'credit_card'

    def __init__(self, bank, token_id):
        self.bank = bank
        self.token_id = token_id

    def serialize(self):
        rv = super(CreditCard, self).serialize()
        rv[self.PAYMENT_TYPE_KEY] = {'bank': self.bank,
                                     'token_id': self.token_id,
                                     }
        return rv


class MandiriClickpay(PaymentTypeBase):
    # http://docs.veritranspay.co.id/sandbox/charge.html#vtdirect-mandiri
    PAYMENT_TYPE_KEY = 'mandiri_clickpay'

    def __init__(self, card_number, input1, input2, input3):
        self.card_number = card_number
        self.input1 = input1
        self.input2 = input2
        self.input3 = input3


class CimbClicks(PaymentTypeBase):
    # http://docs.veritranspay.co.id/sandbox/charge.html#vtdirect-cimb

    PAYMENT_TYPE_KEY = 'cimb_clicks'

    def __init__(self, description):
        self.description = description
