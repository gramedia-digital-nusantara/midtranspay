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


class MandiriClickpayTests(unittest.TestCase):

    def test_init(self):
        card_num = fake.credit_card_number()
        input1 = fake.random_number(digits=6)
        input2 = fake.random_number(digits=6)
        input3 = fake.random_number(digits=6)

        cpay = MandiriClickpay(card_number=card_num,
                               input1=input1,
                               input2=input2,
                               input3=input3)

        self.assertEqual(cpay.card_number, card_num)
        self.assertEqual(cpay.input1, input1)
        self.assertEqual(cpay.input2, input2)
        self.assertEqual(cpay.input3, input3)

    def test_serialization(self):
        self.skipTest("reason")


class CimbClicksTests(unittest.TestCase):

    def test_init(self):
        descr = fake.sentence()
        cimb = CimbClicks(description=descr)
        self.assertEqual(cimb.description, descr)

    def test_serialization(self):
        self.skipTest("reason")
