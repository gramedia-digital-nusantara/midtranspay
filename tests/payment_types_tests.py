import unittest

from faker import Faker

from veritranspay.payment_types import CreditCard, Indomaret


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


class CStoreIndomaretTests(unittest.TestCase):

    def test_init(self):
        message = fake.word()

        indomrt = Indomaret(message=message)

        self.assertEqual(indomrt.store, 'Indomaret')
        self.assertEqual(indomrt.message, message)

    def test_serialization(self):
        message = fake.word()

        indomrt = Indomaret(message=message)

        expected = {
            'payment_type': 'cstore',
            'cstore': {
                'store': 'Indomaret',
                'message': message
            }
        }

        self.assertDictEqual(expected, indomrt.serialize())



