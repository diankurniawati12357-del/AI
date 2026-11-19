"""BIOVA Authentication Service
Handles secure registration, password hashing (PBKDF2-HMAC-SHA256), login, and session validation.
"""

import hashlib
import hmac
import os
import re
from typing import Optional, Dict, Any, Tuple
from services.db import get_connection


def hash_password(password: str) -> str:
    """Hashes a password with a randomly generated salt using PBKDF2-HMAC-SHA256."""
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return f"{salt.hex()}:{key.hex()}"


def verify_password(stored_hash: str, password_attempt: str) -> bool:
    """Verifies a plain password attempt against the stored salt:key string."""
    try:
        salt_hex, key_hex = stored_hash.split(":")
        salt = bytes.fromhex(salt_hex)
        expected_key = bytes.fromhex(key_hex)
        new_key = hashlib.pbkdf2_hmac("sha256", password_attempt.encode("utf-8"), salt, 100000)
        return hmac.compare_digest(expected_key, new_key)
    except Exception:
        return False


def validate_email(email: str) -> bool:
    """Checks whether the provided email conforms to a basic email regex."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email.strip()))


def register_user(username: str, email: str, password: str) -> Tuple[bool, str]:
    """Validates and registers a new user in the SQLite database."""
    username = username.strip()
    email = email.strip().lower()

    if len(username) < 3:
        return False, "Nama pengguna minimal 3 karakter."
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        return False, "Nama pengguna hanya boleh mengandung huruf, angka, dan garis bawah (_)."
    if not validate_email(email):
        return False, "Format email tidak valid."
    if len(password) < 6:
        return False, "Kata sandi minimal 6 karakter."

    pw_hash = hash_password(password)

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            # Check unique username
            cursor.execute("SELECT id FROM users WHERE username = ?;", (username,))
            if cursor.fetchone():
                return False, "Nama pengguna sudah terdaftar. Silakan pilih nama lain."
            # Check unique email
            cursor.execute("SELECT id FROM users WHERE email = ?;", (email,))
            if cursor.fetchone():
                return False, "Email sudah terdaftar. Silakan gunakan email lain."

            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?);",
                (username, email, pw_hash),
            )
            user_id = cursor.lastrowid
            
            # Unlock Chapter 1 by default for both Hewan and Tumbuhan
            cursor.execute(
                "INSERT OR IGNORE INTO chapter_progress (user_id, category, chapter_id, is_unlocked) VALUES (?, 'hewan', 1, 1);",
                (user_id,),
            )
            cursor.execute(
                "INSERT OR IGNORE INTO chapter_progress (user_id, category, chapter_id, is_unlocked) VALUES (?, 'tumbuhan', 1, 1);",
                (user_id,),
            )
            conn.commit()
            return True, "Pendaftaran berhasil! Silakan masuk dengan akun barumu."
    except Exception as e:
        return False, f"Terjadi kesalahan saat mendaftar: {str(e)}"


def authenticate_user(username: str, password: str) -> Tuple[bool, Optional[Dict[str, Any]], str]:
    """Authenticates a user against the database and returns user details on success."""
    username = username.strip()
    if not username or not password:
        return False, None, "Nama pengguna dan kata sandi wajib diisi."

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, email, password_hash, created_at FROM users WHERE username = ?;",
                (username,),
            )
            row = cursor.fetchone()
            if not row:
                return False, None, "Nama pengguna tidak ditemukan."

            stored_hash = row["password_hash"]
            if not verify_password(stored_hash, password):
                return False, None, "Kata sandi salah. Silakan coba lagi."

            # Calculate stars for this user
            cursor.execute(
                "SELECT COALESCE(SUM(stars_awarded), 0) AS total_stars FROM reward_events WHERE user_id = ?;",
                (row["id"],),
            )
            stars_row = cursor.fetchone()
            stars = stars_row["total_stars"] if stars_row else 0

            user_data = {
                "id": row["id"],
                "username": row["username"],
                "email": row["email"],
                "created_at": row["created_at"],
                "stars": stars,
            }
            return True, user_data, "Login berhasil!"
    except Exception as e:
        return False, None, f"Terjadi kesalahan saat login: {str(e)}"


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves current user details including live star tally."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, email, created_at FROM users WHERE id = ?;",
                (user_id,),
            )
            row = cursor.fetchone()
            if not row:
                return None

            cursor.execute(
                "SELECT COALESCE(SUM(stars_awarded), 0) AS total_stars FROM reward_events WHERE user_id = ?;",
                (user_id,),
            )
            stars = cursor.fetchone()["total_stars"]

            return {
                "id": row["id"],
                "username": row["username"],
                "email": row["email"],
                "created_at": row["created_at"],
                "stars": stars,
            }
    except Exception:
        return None
