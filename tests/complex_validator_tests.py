import unittest

from faker import Faker

from veritranspay import validators

fake = Faker()


class AddressVaildator_UnitTests(unittest.TestCase):

    def test_required_address(self):

        v = validators.AddressValidator(is_required=True)

        bad_none = None
        bad_too_long = ''.join([fake.random_letter() for _ in range(201)])

        for bad in [bad_none, bad_too_long]:
            l = lambda: v.validate(bad)
            self.assertRaises(validators.ValidationError, l)

        good_blank = ''
        good_length = ''.join([fake.random_letter() for _ in range(200)])

        for good in [good_blank, good_length]:
            self.assertIsNone(v.validate(good))

    def test_optional_address(self):

        v = validators.AddressValidator(is_required=False)

        bad_too_long = ''.join([fake.random_letter() for _ in range(201)])

        for bad in [bad_too_long]:
            l = lambda: v.validate(bad)
            self.assertRaises(validators.ValidationError, l)

        good_none = None
        good_blank = ''
        good_length = ''.join([fake.random_letter() for _ in range(200)])

        for good in [good_none, good_blank, good_length]:
            self.assertIsNone(v.validate(good))


class PostalCodeValidator_UnitTests(unittest.TestCase):

    def test_accepts_random_postalcodes(self):
        ''' Generates 100 random postal codes and validates them. '''
        v = validators.PostalcodeValidator()
        for pc in [fake.postcode() for _ in range(100)]:
            result = v.validate(pc)
            self.assertIsNone(result)

    def test_pynone_validates_when_isrequired_eq_false(self):
        ''' If is_required=False is provided as a constructor arg,
        a value of None will validate.
        '''
        v = validators.PostalcodeValidator(is_required=False)
        result = v.validate(None)
        self.assertIsNone(result)

    def test_pynone_fails_by_default(self):
        ''' A value of None should fail validation by default '''
        v = validators.PostalcodeValidator()
        l = lambda: v.validate(None)
        self.assertRaises(validators.ValidationError, l)

    def test_long_postal_codes_raise_value_error(self):
        ''' Postal codes can be at most 10 characters long.
        Longer values should raise a ValidationError()
        '''
        v = validators.PostalcodeValidator()
        long_pc = ''.join([str(fake.random_digit()) for _ in range(11)])
        l = lambda: v.validate(long_pc)
        self.assertRaises(validators.ValidationError, l)


class NameValidator_UnitTests(unittest.TestCase):

    def test_accepts_random_cities(self):
        ''' Generates 100 random names and validates them. '''
        v = validators.NameValidator()
        for name in [fake.first_name() for _ in range(100)]:
            result = v.validate(name)
            self.assertIsNone(result)

    def test_raises_value_error_on_names_longer_than_20_chars(self):
        ''' Names can be at most 20 characters long.
        Longer names should raise a ValidationError.
        '''
        v = validators.NameValidator()
        long_name = ''.join([fake.random_letter() for _ in range(21)])
        l = lambda: v.validate(long_name)
        self.assertRaises(validators.ValidationError, l)


class CityValidator_UnitTests(unittest.TestCase):

    def test_accepts_random_cities(self):
        ''' Generates 100 random cities and validates them. '''
        v = validators.CityValidator()
        for city in [fake.city() for _ in range(100)]:
            # note: some city names are longer than 20 letters
            if len(city) > 20:
                continue
            result = v.validate(city)
            self.assertIsNone(result)

    def test_raises_value_error_on_names_longer_than_20_chars(self):
        ''' City names can be at most 20 characters long.
        Longer names should raise a ValidationError.
        '''
        v = validators.CityValidator()
        long_city = ''.join([fake.random_letter() for _ in range(21)])
        l = lambda: v.validate(long_city)
        self.assertRaises(validators.ValidationError, l)


class PhoneValidator_UnitTests(unittest.TestCase):

    def test_accepts_random_phone_numbers(self):
        '''
        Note: some of the phone numbers provided by our fake library
        won't validate here!  They contain an extension portion, which the
        API won't accept, so we have to split them off manually.
        '''
        v = validators.PhoneValidator()
        for phonenum in [fake.phone_number().split('x')[0] for _
                         in range(100)]:
            # TODO: exclude formats with '.' by providing locale
            # for now, just skipping them manually
            if '.' in list(phonenum):
                continue
            result = v.validate(phonenum)
            self.assertIsNone(result)

    def test_bad_input_raises_ValidationError(self):
        '''
        Phone numbers are documented as accepting only the following
        characters: 0 through 9, +, -, space, and left+right parenthesis (,).
        Any other characters provided should raise a validation error.
        '''
        v = validators.PhoneValidator()

        # this is all the characters that we're capiable of accepting
        accepted_chars = ['+',
                          '-',
                          ' ',
                          '(',
                          ')',
                          ] + [str(dig) for dig in range(10)]

        # faker sometimes provides us with phone numbers that are too long
        # or contain an extension portion -- we want to find and USE those
        # invalid format numbers for our tests
        bad_nums = []
        for phone_num in [fake.phone_number() for _ in range(100)]:
            digs = list(phone_num)
            for d in digs:
                if d not in accepted_chars:
                    bad_nums.append(phone_num)
                    continue

        if not bad_nums:
            self.skipTest("WARNING! We didn't generate any invalid phone "
                          "numbers to test against?  You should probably "
                          "rerun these tests")
        for bad in bad_nums:
            l = lambda: v.validate(bad)
            self.assertRaises(validators.ValidationError, l)

    def test_min_length(self):
        v = validators.PhoneValidator()
        too_short = ''.join([str(fake.random_digit()) for _ in range(4)])
        l = lambda: v.validate(too_short)
        self.assertRaises(validators.ValidationError, l)

    def test_max_length(self):
        v = validators.PhoneValidator()
        too_long = ''.join(str(fake.random_digit()) for _ in range(20))
        l = lambda: v.validate(too_long)
        self.assertRaises(validators.ValidationError, l)


class EmailValidator_UnitTests(unittest.TestCase):

    def test_validate_emails(self):
        v = validators.EmailValidator()
        for email in [fake.email() for _ in range(100)]:
            result = v.validate(email)
            self.assertIsNone(result)


class CountrycodeValidator_UnitTests(unittest.TestCase):

    def test(self):
        self.skipTest("Implement me!")


class OrderidValidator_UnitTests(unittest.TestCase):
    def test(self):
        self.skipTest("Implement me!")
