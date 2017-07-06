# import unittest
#
# from faker import Faker
#
# from midtranspay import request
# from midtranspay.request import TransactionDetails
#
#
# fake = Faker()
#
#
# class Request_TransactionDetails_UnitTests(unittest.TestCase):
#
#     def setUp(self):
#         self.order_id = fake.random_letter() * 10
#         self.gross_amount = fake.random_number()
#
#         self.complete_td = \
#             request.TransactionDetails(order_id=self.order_id,
#                                        gross_amount=self.gross_amount)
#
#     def test_init_sets_attributes(self):
#
#         oid = self.order_id
#         amt = self.gross_amount
#
#         td = request.TransactionDetails(order_id=oid, gross_amount=amt)
#
#         self.assertEqual(td.order_id, oid)
#         self.assertEqual(td.gross_amount, amt)
#
#     def test_validation_order_id(self):
#
#         pattern = TransactionDetails._validators['order_id']
#         td = self.complete_td
#
#         self.assertIsNone(
#             td.validate_attr(
#                 'order_id',
#                 "".join([fake.random_letter() for _ in range(10)]),
#                 pattern))
#
#         bad_blank = ''
#         bad_too_long = ''.join([fake.random_letter() for _ in range(51)])
#
#         for bad in [bad_blank, bad_too_long]:
#             self.assertRaises(ValueError, lambda: td.validate_attr('order_id',
#                                                                    bad,
#                                                                    pattern))
#
#     def test_validate_gross_amount(self):
#
#         pattern = TransactionDetails._validators['gross_amount']
#         td = self.complete_td
#
#         self.assertIsNone(td.validate_attr('gross_amount',
#                                            fake.random_number(),
#                                            pattern))
#
#         bad_chars = fake.random_letter()
#         bad_blank = ''
#         bad_stringified_number = '99.99'
#
#         for bad in [bad_chars, bad_blank, bad_stringified_number]:
#             self.assertRaises(ValueError,
#                               lambda: td.validate_attr('gross_amount',
#                                                        bad,
#                                                        pattern))
