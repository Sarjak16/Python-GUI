import unittest
from utils.security import hash_password, verify_password

class TestSecurity(unittest.TestCase):

    def test_hash_password(self):
        password = "abc123"
        hashed = hash_password(password)
        self.assertNotEqual(password, hashed)
        self.assertEqual(len(hashed), 64)

    def test_verify_password_success(self):
        password = "abc123"
        hashed = hash_password(password)
        self.assertTrue(verify_password("abc123", hashed))

    def test_verify_password_fail(self):
        hashed = hash_password("abc123")
        self.assertFalse(verify_password("wrongpass", hashed))

if __name__ == "__main__":
    unittest.main()
