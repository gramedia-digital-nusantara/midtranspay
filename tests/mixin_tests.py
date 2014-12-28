import unittest

from mock import MagicMock

from veritranspay import mixins


class ValidatableMixin_UnitTests(unittest.TestCase):

    def test_validate_attr_calls_validate_as_expected(self):
        self.skipTest("")

    def test_validate_attr_raises_validation_error(self):
        self.skipTest("")

    def test_validate_attr_validation_error_message_format(self):
        self.skipTest("")

    def test_validate_attr_raises_other_errors(self):
        self.skipTest("")

    def test_validate_all_hits_all_validators(self):
        self.skipTest("")


class SerializableMixin_UnitTests(unittest.TestCase):

    def test_serialize_returns_expected(self):

        obj_with_ser = MagicMock(spec=object)
        mock_serialize = MagicMock(return_value={'a':'b'})
        obj_with_ser.attach_mock(mock_serialize, 'serialize')

        obj_without_ser = MagicMock(spec=object)

        class ICanSerialize(mixins.SerializableMixin):
            def __init__(self):
                self.attr1 = obj_with_ser
                self.attr2 = obj_without_ser

        serialize_me = ICanSerialize()

        actual = serialize_me.serialize()

        expected = {'attr1': {'a':'b', },
                    'attr2': obj_without_ser,
                    }

        self.assertEqual(actual, expected)
        mock_serialize.assert_any_call()


class RequestEntityMixin_UnitTests(unittest.TestCase):

    def test_returns_expected_string_representation(self):

        class HiThere(mixins.RequestEntity):
            pass

        hi = HiThere()

        expected = "<HiThere()>"
        actual = str(hi)
        self.assertEqual(actual, expected)

        actual = repr(hi)
        self.assertEqual(actual, expected)



