import unittest

from faker import Faker

from veritranspay.payment_types import CreditCard, MandiriClickpay, CimbClicks


fake = Faker()


class CreditCardTests(unittest.TestCase):

    def test_init(self):
        ''' Makes sure the expected attributes are required, and
        persisted as instance attributes.
        '''
        bank = fake.word()
        token_id = fake.word()

        cc = CreditCard(bank=bank, token_id=token_id)

        self.assertEqual(cc.bank, bank)
        self.assertEqual(cc.token_id, token_id)

    def test_serialization(self):
        bank = fake.word()
        token_id = fake.word()

        cc = CreditCard(bank=bank, token_id=token_id)

        serialized = cc.serialize()
        expected = {'payment_type': CreditCard.PAYMENT_TYPE_KEY,
                    CreditCard.PAYMENT_TYPE_KEY: {
                        'bank': bank,
                        'token_id': token_id,
                    }}

        self.assertEqual(serialized, expected)

