import unittest

from mock import MagicMock
from faker import Faker

from veritranspay import mixins, validators


fake = Faker()


class ValidatableMixin_UnitTests(unittest.TestCase):

    def setUp(self):
        self.name = ''.join([fake.random_letter() for _ in range(20)])
        self.value = ''.join([fake.random_letter() for _ in range(20)])
        self.mock_validator = MagicMock()
        self.mock_validate_method = MagicMock()
        self.mock_validator.attach_mock(self.mock_validate_method,
                                        'validate')

    def test_validate_attr_calls_validate_as_expected(self):
        mixin = mixins.ValidatableMixin()
        mixin.validate_attr(self.name, self.value, self.mock_validator)

        self.mock_validate_method.assert_called_once_with(self.value)

    def test_validate_attr_raises_validation_error(self):
        mixin = mixins.ValidatableMixin()

        self.mock_validate_method.side_effect = validators.ValidationError()

        self.assertRaises(validators.ValidationError,
                          lambda: mixin.validate_attr(
                              self.name,
                              self.value,
                              self.mock_validator))

    def test_validate_attr_validation_error_message_format(self):
        mixin = mixins.ValidatableMixin()

        self.mock_validate_method.side_effect = \
            validators.ValidationError("I'm a little tea pot")

        try:
            mixin.validate_attr(
                self.name,
                self.value,
                self.mock_validator)
        except validators.ValidationError as e:
            self.assertEqual(e.message,
                             "{name} failed validation: {msg}".format(
                                 name=self.name,
                                 msg="I'm a little tea pot"))

    def test_validate_attr_raises_other_errors(self):
        mixin = mixins.ValidatableMixin()

        self.mock_validate_method.side_effect = TypeError()

        self.assertRaises(TypeError,
                          lambda: mixin.validate_attr(
                              self.name,
                              self.value,
                              self.mock_validator))

    def test_validate_all_hits_all_validators(self):
        self.skipTest("Not implemented")


class SerializableMixin_UnitTests(unittest.TestCase):

    def test_serialize_returns_expected(self):

        obj_with_ser = MagicMock(spec=object)
        mock_serialize = MagicMock(return_value={'a': 'b'})
        obj_with_ser.attach_mock(mock_serialize, 'serialize')

        obj_without_ser = MagicMock(spec=object)

        class ICanSerialize(mixins.SerializableMixin):
            def __init__(self):
                self.attr1 = obj_with_ser
                self.attr2 = obj_without_ser

        serialize_me = ICanSerialize()

        actual = serialize_me.serialize()

        expected = {'attr1': {'a': 'b', },
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
