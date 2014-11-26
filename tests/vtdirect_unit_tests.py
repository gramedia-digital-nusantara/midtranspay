import unittest

from faker import Faker

from veritrans.veritrans import VTDirect


fake = Faker()

class VTDirect_Init_Tests(unittest.TestCase):

    def setUp(self):
        self.server_key = fake.word()
        super(VTDirect_Init_Tests, self).setUp()

    def test_requires_server_key(self):
        ''' server_key should be a required parameter. '''
        self.assertRaises(TypeError, VTDirect, msg="")
    
    def test_instance_attributes_set(self):
        v = VTDirect(server_key=self.server_key)
        self.assertEqual(v.server_key, self.server_key, "")
        self.assertFalse(v.sandbox_mode, "")
    
    def test_sanbox_mode_set_as_attribute(self):
        v = VTDirect(server_key=self.server_key, sandbox_mode=True)
        self.assertEqual(v.server_key, self.server_key, "")
        self.assertTrue(v.sandbox_mode, "")
        
    def test_sandbox_mode_expected_url(self):
        expected_url = 'https://api.sandbox.veritrans.co.id/v2'
        v = VTDirect(server_key=self.server_key, sandbox_mode=True)
        self.assertEqual(v.base_url, expected_url)
        
    def test_live_mode_expected_url(self):
        expected_url = 'https://api.veritrans.co.id/v2'
        v = VTDirect(server_key=self.server_key, sandbox_mode=False)
        self.assertEqual(v.base_url, expected_url)