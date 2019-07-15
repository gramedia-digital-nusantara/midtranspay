from . import mixins


class PaymentTypeBase(mixins.SerializableMixin):
    '''
    Base type for all payment types.  Not usable by itself.
    '''
    def serialize(self):
        return {"payment_type": self.PAYMENT_TYPE_KEY,
                self.PAYMENT_TYPE_KEY: {},
                }


class CreditCard(PaymentTypeBase):
    '''
    A payment made with a credit card.
    http://docs.veritranspay.co.id/sandbox/charge.html#vtdirect-cc
    '''
    PAYMENT_TYPE_KEY = 'credit_card'

    def __init__(self, bank, token_id, save_token_id=False, bins=None):
        '''
        :param bank: Represents the acquiring bank.
        :type bank: :py:class:`str`
        :param token_id: A token retrieved from the Veritrans
            JavaScript library, after submitting the credit card details.
        :type token_id: :py:class:`str`
        :param bool save_token_id: Used in conjunction with a 2-click to
            indicate whether or not this token is to be made reusable.
        '''
        self.bank = bank
        self.token_id = token_id
        self.save_token_id = save_token_id
        self.bins = bins

    def serialize(self):

        rv = super(CreditCard, self).serialize()

        rv[self.PAYMENT_TYPE_KEY] = {'bank': self.bank,
                                     'token_id': self.token_id,
                                     }

        # append save_token_id to the request, only if it's set to True
        if self.save_token_id:
            rv[self.PAYMENT_TYPE_KEY].update(
                {'save_token_id': self.save_token_id})

        if self.bins:
            rv[self.PAYMENT_TYPE_KEY].update({
                'bins': self.bins
            })

        return rv


class Indomaret(PaymentTypeBase):
    PAYMENT_TYPE_KEY = 'cstore'

    def __init__(self, message):
        self.store = 'Indomaret'
        self.message = message

    def serialize(self):
        rv = super(Indomaret, self).serialize()
        rv[self.PAYMENT_TYPE_KEY].update({
            'store': self.store,
            'message': self.message
        })
        return rv


class VirtualAccount(PaymentTypeBase, mixins.SerializableMixin):
    """
        Base class for payment using virtual account
    """
    PAYMENT_TYPE_KEY = 'bank_transfer'

    def serialize(self):
        rv = super(VirtualAccount, self).serialize()
        rv[self.PAYMENT_TYPE_KEY].update({
           'bank': self.bank
        })
        return rv


class VirtualAccountPermata(VirtualAccount):
    """
    A payment made with a virtual account Permata.

    https://api-docs.midtrans.com/#permata-virtual-account
    """
    def __init__(self):
        self.bank = 'permata'


class VirtualAccountBca(VirtualAccount):
    """
    A payment made with a virtual account BCA.
    NOTE: untested in sandbox, not available
    https://api-docs.midtrans.com/#bca-virtual-account
    """
    def __init__(self):
        self.bank = 'bca'


class VirtualAccountBni(VirtualAccount):
    """
    A payment made with a virtual account BNI
    NOTE: untested in sandbox, not available
    https://api-docs.midtrans.com/#bni-virtual-account
    """
    def __init__(self):
        self.bank = 'bni'


class VirtualAccountMandiri(PaymentTypeBase):
    """
     A payment made with a virtual account Mandiri (BillPayment Mandiri)

    https://api-docs.midtrans.com/#mandiri-bill-payment
    """
    PAYMENT_TYPE_KEY = 'echannel'

    def __init__(self, bill_info1, bill_info2):
        self.bill_info1 = bill_info1
        self.bill_info2 = bill_info2

    def serialize(self):
        rv = super(VirtualAccountMandiri, self).serialize()
        rv[self.PAYMENT_TYPE_KEY].update({
            'bill_info1': self.bill_info1,
            'bill_info2': self.bill_info2
        })
        return rv


class BriEpay(PaymentTypeBase):
    """
    A payment made with a Epay BRI

    https://api-docs.midtrans.com/#epay-bri
    """
    PAYMENT_TYPE_KEY = 'bri_epay'


class MandiriClickpay(PaymentTypeBase):
    """
    A payment made with a Mandiri Click Pay.

    http://api-docs.midtrans.com/#mandiri-clickpay
    """
    PAYMENT_TYPE_KEY = 'mandiri_clickpay'

    def __init__(self, card_number, input1, input2, input3, token):
        self.card_number = card_number
        self.input1 = input1
        self.input2 = input2
        self.input3 = input3
        self.token = token

    def serialize(self):
        rv = super(MandiriClickpay, self).serialize()
        rv[self.PAYMENT_TYPE_KEY].update({
            'card_number': self.card_number,
            'input1': self.input1,
            'input2': self.input2,
            'input3': self.input3,
            'token': self.token
        })

        return rv


class CimbClicks(PaymentTypeBase):
    """
    A payment made with a Cimb Clicks.

    http://api-docs.midtrans.com/#cimb-clicks
    """

    PAYMENT_TYPE_KEY = 'cimb_clicks'

    def __init__(self, description):
        self.description = description

    def serialize(self):
        rv = super(CimbClicks, self).serialize()
        rv[self.PAYMENT_TYPE_KEY].update({
            'description': self.description
        })

        return rv


class BCAKlikPay(PaymentTypeBase):
    """
    A payment made with a BCA Klik Pay.

    http://api-docs.midtrans.com/#bca-klikpay
    """
    PAYMENT_TYPE_KEY = 'bca_klikpay'

    def __init__(self, type_id, description):
        self.type = type_id
        self.description = description

    def serialize(self):
        rv = super(BCAKlikPay, self).serialize()
        rv[self.PAYMENT_TYPE_KEY].update({
            'type': self.type,
            'description': self.description
        })

        return rv


class KlikBCA(PaymentTypeBase):
    """
    A payment made with a BCA Klik Pay.

    http://api-docs.midtrans.com/#klikbca
    """
    PAYMENT_TYPE_KEY = 'bca_klikbca'

    def __init__(self, user_id, description):
        self.user_id = user_id
        self.description = description

    def serialize(self):
        rv = super(KlikBCA, self).serialize()
        rv[self.PAYMENT_TYPE_KEY].update({
            'user_id': self.user_id,
            'description': self.description})

        return rv


class GoPay(PaymentTypeBase):
    """
    A payment made with a BCA Klik Pay.

    https://api-docs.midtrans.com/#go-pay
    """
    PAYMENT_TYPE_KEY = 'gopay'