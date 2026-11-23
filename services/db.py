"""BIOVA Database Service
Handles SQLite database connection, table initialization, and transactions.
"""

import sqlite3
from typing import Optional
from services.config import DB_PATH


def get_connection() -> sqlite3.Connection:
    """Returns a SQLite connection with foreign keys enabled and row factory set."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    """Initializes all required SQLite tables if they do not exist."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Additive migrations for bilingual profiles and provider identities.
        cursor.execute("PRAGMA table_info(users);")
        user_columns = {row["name"] for row in cursor.fetchall()}
        if "language" not in user_columns:
            cursor.execute("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'id';")
        if "auth_provider" not in user_columns:
            cursor.execute("ALTER TABLE users ADD COLUMN auth_provider TEXT DEFAULT 'local';")
        if "provider_subject" not in user_columns:
            cursor.execute("ALTER TABLE users ADD COLUMN provider_subject TEXT;")
        if "profile_photo_path" not in user_columns:
            cursor.execute("ALTER TABLE users ADD COLUMN profile_photo_path TEXT;")

        # Classification history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS classification_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                predicted_group TEXT,
                predicted_species TEXT,
                confidence REAL,
                model_version TEXT,
                image_hash TEXT,
                classification_status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            );
        """)

        # Quiz attempts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                chapter_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            );
        """)

        # Chapter progress table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chapter_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                chapter_id INTEGER NOT NULL,
                best_score INTEGER DEFAULT 0,
                is_unlocked BOOLEAN DEFAULT 0,
                is_completed BOOLEAN DEFAULT 0,
                UNIQUE(user_id, category, chapter_id),
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS material_progress (
                user_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                material_id TEXT NOT NULL,
                is_completed BOOLEAN NOT NULL DEFAULT 1,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, category, material_id),
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            );
        """)

        # Reward events table for stars and gamification
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reward_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                reward_type TEXT NOT NULL,
                reference_id TEXT NOT NULL,
                stars_awarded INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, reward_type, reference_id),
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            );
        """)

        # Species catalog table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS species_catalog (
                id TEXT PRIMARY KEY,
                common_name TEXT NOT NULL,
                scientific_name TEXT NOT NULL,
                category TEXT NOT NULL,
                group_name TEXT NOT NULL,
                description TEXT NOT NULL,
                habitat TEXT,
                image_path TEXT,
                model_3d_path TEXT,
                has_animation BOOLEAN DEFAULT 0,
                verification_status TEXT DEFAULT 'verified'
            );
        """)

        conn.commit()


# Run initialization on import safely
init_db()
