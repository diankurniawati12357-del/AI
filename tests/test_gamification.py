"""Unit tests for BIOVA Gamification & Leaderboard Services."""

import unittest
import uuid
from services.auth_service import register_user, authenticate_user
from services.game_service import (
    calculate_tier,
    award_upload_star,
    award_quiz_rewards,
    get_user_stats,
    get_chapter_progress,
)
from services.leaderboard_service import get_leaderboard, get_user_rank


class TestGamificationService(unittest.TestCase):
    def test_tier_calculation(self):
        self.assertEqual(calculate_tier(0, 0)["name"], "Bronze")
        self.assertEqual(calculate_tier(19, 5)["name"], "Bronze")
        self.assertEqual(calculate_tier(20, 2)["name"], "Silver")
        self.assertEqual(calculate_tier(59, 10)["name"], "Silver")
        self.assertEqual(calculate_tier(60, 15)["name"], "Gold")
        self.assertEqual(calculate_tier(99, 18)["name"], "Gold")
        # 100 stars but < 20 uploads -> remains Gold
        self.assertEqual(calculate_tier(100, 15)["name"], "Gold")
        # 100 stars AND >= 20 uploads -> Platinum!
        self.assertEqual(calculate_tier(100, 20)["name"], "Platinum")
        self.assertEqual(calculate_tier(150, 25)["name"], "Platinum")

    def test_star_reward_and_anti_duplication(self):
        unique_name = f"gamer_{uuid.uuid4().hex[:6]}"
        register_user(unique_name, f"{unique_name}@unesa.ac.id", "Password123!")
        _, user, _ = authenticate_user(unique_name, "Password123!")
        user_id = user["id"]

        # 1. Unique upload reward
        hash1 = f"img_hash_{uuid.uuid4().hex}"
        awarded_first = award_upload_star(user_id, hash1)
        self.assertTrue(awarded_first, "First upload should award 1 star")

        # Duplicate upload with same hash should NOT award another star
        awarded_second = award_upload_star(user_id, hash1)
        self.assertFalse(awarded_second, "Duplicate upload should NOT award a star")

        # 2. Quiz reward: 4 correct answers
        stars_quiz1 = award_quiz_rewards(user_id, "hewan", chapter_id=1, score=4, max_questions=5)
        self.assertEqual(stars_quiz1, 4, "4 correct questions should award 4 stars")

        # Repeating quiz with same or lower score shouldn't award duplicate question stars
        stars_quiz_repeat = award_quiz_rewards(user_id, "hewan", chapter_id=1, score=3, max_questions=5)
        self.assertEqual(stars_quiz_repeat, 0, "Repeated quiz with lower score should award 0 new stars")

        # Improving score to 5/5 -> +1 new question star and +3 perfect score bonus = +4 stars!
        stars_perfect = award_quiz_rewards(user_id, "hewan", chapter_id=1, score=5, max_questions=5)
        self.assertEqual(stars_perfect, 4, "Reaching 5/5 should award 1 new question star + 3 bonus stars")

        # Check total stars: 1 (upload) + 4 (first quiz) + 4 (improvement + bonus) = 9 stars
        stats = get_user_stats(user_id)
        self.assertEqual(stats["stars"], 9)

        # Check Chapter 2 is unlocked because score >= 3
        prog = get_chapter_progress(user_id, "hewan")
        self.assertTrue(prog[2]["is_unlocked"], "Chapter 2 should be unlocked after passing Chapter 1")

    def test_leaderboard_ordering(self):
        board = get_leaderboard(limit=10)
        self.assertIsInstance(board, list)
        if len(board) >= 2:
            # Check descending order of stars
            for i in range(len(board) - 1):
                self.assertGreaterEqual(board[i]["stars"], board[i + 1]["stars"])


if __name__ == "__main__":
    unittest.main()
