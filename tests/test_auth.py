"""Unit tests for BIOVA Authentication Service."""

import unittest
import uuid
from services.auth_service import (
    hash_password,
    verify_password,
    validate_email,
    register_user,
    authenticate_user,
)


class TestAuthService(unittest.TestCase):
    def test_password_hashing(self):
        pwd = "SecretPassword123!"
        hashed = hash_password(pwd)
        self.assertIn(":", hashed)
        self.assertTrue(verify_password(hashed, pwd))
        self.assertFalse(verify_password(hashed, "WrongPassword"))

    def test_validate_email(self):
        self.assertTrue(validate_email("test@unesa.ac.id"))
        self.assertTrue(validate_email("user.name123@gmail.com"))
        self.assertFalse(validate_email("invalid-email"))
        self.assertFalse(validate_email("@missinguser.com"))
        self.assertFalse(validate_email("no_at_sign.com"))

    def test_registration_and_login_flow(self):
        unique_suffix = str(uuid.uuid4())[:8]
        username = f"test_{unique_suffix}"
        email = f"test_{unique_suffix}@unesa.ac.id"
        password = "ValidPassword123"

        # 1. Successful registration
        ok, msg = register_user(username, email, password)
        self.assertTrue(ok, f"Registration failed: {msg}")

        # 2. Duplicate username should fail
        dup_ok, dup_msg = register_user(username, f"other_{unique_suffix}@unesa.ac.id", password)
        self.assertFalse(dup_ok)
        self.assertIn("sudah terdaftar", dup_msg.lower())

        # 3. Duplicate email should fail
        dup_email_ok, dup_email_msg = register_user(f"other_{unique_suffix}", email, password)
        self.assertFalse(dup_email_ok)
        self.assertIn("sudah terdaftar", dup_email_msg.lower())

        # 4. Successful login
        login_ok, user_data, login_msg = authenticate_user(username, password)
        self.assertTrue(login_ok)
        self.assertIsNotNone(user_data)
        self.assertEqual(user_data["username"], username)

        # 5. Wrong password should fail
        wrong_ok, _, wrong_msg = authenticate_user(username, "WrongPassword!")
        self.assertFalse(wrong_ok)
        self.assertIn("salah", wrong_msg.lower())

        # 6. Non-existent username should fail
        none_ok, _, none_msg = authenticate_user(f"non_existent_{unique_suffix}", password)
        self.assertFalse(none_ok)
        self.assertIn("tidak ditemukan", none_msg.lower())


if __name__ == "__main__":
    unittest.main()
