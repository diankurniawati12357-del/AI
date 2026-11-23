"""Isolated tests for BIOVA progress, rewards, and leaderboard services."""

import sqlite3
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

from services.game_service import (
    award_quiz_rewards,
    award_upload_star,
    calculate_tier,
    get_material_progress,
    get_user_stats,
    mark_material_completed,
)
from services.leaderboard_service import get_leaderboard, get_user_rank


class TestGamificationService(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_dir.name) / "biova-test.db"

        @contextmanager
        def connect():
            connection = sqlite3.connect(self.database_path)
            connection.row_factory = sqlite3.Row
            try:
                yield connection
            finally:
                connection.close()

        self.connect = connect
        self.game_connection_patch = patch("services.game_service.get_connection", side_effect=connect)
        self.leaderboard_connection_patch = patch(
            "services.leaderboard_service.get_connection", side_effect=connect
        )
        self.game_connection_patch.start()
        self.leaderboard_connection_patch.start()
        with self.connect() as connection:
            connection.executescript(
                """
                CREATE TABLE reward_events (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    reward_type TEXT NOT NULL,
                    reference_id TEXT NOT NULL,
                    stars_awarded INTEGER NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, reward_type, reference_id)
                );
                CREATE TABLE quiz_attempts (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    chapter_id INTEGER NOT NULL,
                    score INTEGER NOT NULL
                );
                CREATE TABLE material_progress (
                    user_id INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    material_id TEXT NOT NULL,
                    is_completed INTEGER NOT NULL DEFAULT 1,
                    PRIMARY KEY(user_id, category, material_id)
                );
                CREATE TABLE chapter_progress (
                    user_id INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    chapter_id INTEGER NOT NULL,
                    best_score INTEGER NOT NULL,
                    is_unlocked INTEGER NOT NULL,
                    is_completed INTEGER NOT NULL
                );
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            connection.execute(
                "INSERT INTO chapter_progress VALUES (1, 'hewan', 2, 4, 1, 1);"
            )
            connection.commit()

    def tearDown(self):
        self.game_connection_patch.stop()
        self.leaderboard_connection_patch.stop()
        self.temp_dir.cleanup()

    def test_tier_calculation(self):
        self.assertEqual(calculate_tier(0, 0)["name"], "Bronze")
        self.assertEqual(calculate_tier(20, 2)["name"], "Silver")
        self.assertEqual(calculate_tier(60, 15)["name"], "Gold")
        self.assertEqual(calculate_tier(100, 20)["name"], "Platinum")

    def test_question_rewards_are_idempotent_and_preserve_legacy_progress(self):
        self.assertTrue(award_upload_star(1, "unique-image"))
        self.assertFalse(award_upload_star(1, "unique-image"))

        self.assertEqual(
            award_quiz_rewards(
                1, "hewan", score=4, question_ids=["q1", "q2", "q3", "q4"]
            ),
            4,
        )
        self.assertEqual(
            award_quiz_rewards(1, "hewan", score=3, question_ids=["q1", "q2", "q3"]),
            0,
        )
        self.assertEqual(
            award_quiz_rewards(
                1, "hewan", score=5, question_ids=["q1", "q2", "q3", "q4", "q5"]
            ),
            4,
        )
        self.assertEqual(
            award_quiz_rewards(
                1, "hewan", score=5, question_ids=["q1", "q2", "q3", "q4", "q5"]
            ),
            0,
        )
        self.assertEqual(get_user_stats(1)["stars"], 9)

        with self.connect() as connection:
            legacy = connection.execute(
                "SELECT best_score, is_unlocked, is_completed FROM chapter_progress "
                "WHERE user_id = 1 AND category = 'hewan' AND chapter_id = 2;"
            ).fetchone()
            attempts = connection.execute(
                "SELECT COUNT(*) AS count FROM quiz_attempts WHERE user_id = 1;"
            ).fetchone()["count"]
        self.assertEqual(tuple(legacy), (4, 1, 1))
        self.assertEqual(attempts, 4)

    def test_legacy_reward_reference_does_not_award_stars_twice(self):
        with self.connect() as connection:
            connection.execute(
                "INSERT INTO reward_events (user_id, reward_type, reference_id, stars_awarded) "
                "VALUES (1, 'quiz_question', 'hewan_1_q1', 1);"
            )
            connection.commit()
        self.assertEqual(
            award_quiz_rewards(1, "hewan", chapter_id=1, score=1),
            0,
        )

    def test_material_completion_is_persisted_by_card_id(self):
        self.assertTrue(mark_material_completed(1, "hewan", "mamalia"))
        self.assertFalse(mark_material_completed(1, "hewan", "mamalia"))
        self.assertEqual(get_material_progress(1, "hewan"), {"mamalia"})
        self.assertEqual(get_user_stats(1)["completed_material"], 1)

    def test_leaderboard_is_sorted_by_stars_and_ranked(self):
        with self.connect() as connection:
            connection.executemany(
                "INSERT INTO users (id, username) VALUES (?, ?);",
                [(1, "first"), (2, "second")],
            )
            connection.executemany(
                "INSERT INTO reward_events (user_id, reward_type, reference_id, stars_awarded) "
                "VALUES (?, 'quiz_question', ?, ?);",
                [(1, "a", 3), (2, "b", 8)],
            )
            connection.commit()
        board = get_leaderboard(limit=10)
        self.assertEqual([row["user_id"] for row in board[:2]], [2, 1])
        self.assertEqual(get_user_rank(1), 2)

    def test_leaderboard_can_return_every_user_for_paged_display(self):
        with self.connect() as connection:
            connection.executemany(
                "INSERT INTO users (id, username) VALUES (?, ?);",
                [(1, "first"), (2, "second"), (3, "third")],
            )
            connection.commit()

        self.assertEqual(len(get_leaderboard(limit=1)), 1)
        self.assertEqual(
            [row["user_id"] for row in get_leaderboard(limit=None)],
            [1, 2, 3],
        )


if __name__ == "__main__":
    unittest.main()
