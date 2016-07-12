from . import mixins


class PaymentTypeBase(mixins.SerializableMixin):
    """ Base type for all payment types.  Not usable by itself.
    """
    def serialize(self):
        return {"payment_type": self.PAYMENT_TYPE_KEY,
                self.PAYMENT_TYPE_KEY: {},
                }


class CreditCard(PaymentTypeBase):
    """ A payment made with a credit card.

    http://docs.veritranspay.co.id/sandbox/charge.html#vtdirect-cc
    """
    PAYMENT_TYPE_KEY = 'credit_card'

    def __init__(self, bank, token_id, save_token_id=False):
        """
        :param `six.string_types` bank: Represents the acquiring bank.
        :param `six.string_types` token_id:
            A token retrieved from the Veritrans JavaScript library, after submitting the credit card details.
        :param `bool` save_token_id:
            Used in conjunction with a 2-click to indicate whether or not this token is to be made reusable.
        """
        self.bank = bank
        self.token_id = token_id
        self.save_token_id = save_token_id

    def serialize(self):

        rv = super(CreditCard, self).serialize()

        rv[self.PAYMENT_TYPE_KEY] = {'bank': self.bank,
                                     'token_id': self.token_id,
                                     }

        # append save_token_id to the request, only if it's set to True
        if self.save_token_id:
            rv[self.PAYMENT_TYPE_KEY].update({'save_token_id': self.save_token_id})

        return rv


class Indomaret(PaymentTypeBase):
    """ Payment that must be completed at a later point in time by the customer at an Indomaret.

    http://docs.veritrans.co.id/en/vtdirect/integration_indomrt.html
    """
    PAYMENT_TYPE_KEY = 'cstore'

    def __init__(self, message):
        """
        :param `six.string_types` message: Label to be displayed in Indomaret POS
        """
        self.store = 'Indomaret'
        self.message = message

    def serialize(self):
        rv = super(Indomaret, self).serialize()
        rv[self.PAYMENT_TYPE_KEY].update({
            'store': self.store,
            'message': self.message
        })
        return rv


class MandiriClickpay(PaymentTypeBase):
    # http://docs.veritranspay.co.id/sandbox/charge.html#vtdirect-mandiri
    PAYMENT_TYPE_KEY = 'mandiri_clickpay'

    def __init__(self, card_number, input1, input2, input3):
        raise NotImplementedError("This payment type is not supported.")

class CimbClicks(PaymentTypeBase):
    # http://docs.veritranspay.co.id/sandbox/charge.html#vtdirect-cimb
    PAYMENT_TYPE_KEY = 'cimb_clicks'

    def __init__(self, description):
        raise NotImplementedError("This payment type is not supported.")
