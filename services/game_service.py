"""BIOVA Gamification & Progress Service
Manages star calculation, tier leveling, reward events, and chapter unlocking.
"""

from typing import Tuple, Dict, Any, List
from services.db import get_connection


def calculate_tier(stars: int, valid_upload_count: int = 0) -> Dict[str, str]:
    """Calculates user tier based on stars count and verified uploads."""
    if stars >= 100 and valid_upload_count >= 20:
        return {
            "name": "Platinum",
            "icon": "💎",
            "color": "#795290",
            "next_threshold": None,
            "stars_needed": 0,
        }
    elif stars >= 60:
        return {
            "name": "Gold",
            "icon": "🥇",
            "color": "#D4AF37",
            "next_threshold": 100,
            "stars_needed": max(0, 100 - stars),
        }
    elif stars >= 20:
        return {
            "name": "Silver",
            "icon": "🥈",
            "color": "#A0A0A0",
            "next_threshold": 60,
            "stars_needed": max(0, 60 - stars),
        }
    else:
        return {
            "name": "Bronze",
            "icon": "🥉",
            "color": "#CD7F32",
            "next_threshold": 20,
            "stars_needed": max(0, 20 - stars),
        }


def get_user_stats(user_id: int) -> Dict[str, Any]:
    """Returns aggregated stats for a user: total stars, tier, counts, and chapter progress."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Total stars
        cursor.execute(
            "SELECT COALESCE(SUM(stars_awarded), 0) AS stars FROM reward_events WHERE user_id = ?;",
            (user_id,),
        )
        stars = cursor.fetchone()["stars"]

        # Valid upload count
        cursor.execute(
            "SELECT COUNT(*) AS upload_count FROM reward_events WHERE user_id = ? AND reward_type = 'upload';",
            (user_id,),
        )
        upload_count = cursor.fetchone()["upload_count"]

        # Quiz attempts
        cursor.execute(
            "SELECT COUNT(*) AS quiz_count FROM quiz_attempts WHERE user_id = ?;",
            (user_id,),
        )
        quiz_count = cursor.fetchone()["quiz_count"]

        tier_info = calculate_tier(stars, upload_count)

        return {
            "stars": stars,
            "tier": tier_info["name"],
            "tier_icon": tier_info["icon"],
            "tier_color": tier_info["color"],
            "stars_needed": tier_info["stars_needed"],
            "upload_count": upload_count,
            "quiz_count": quiz_count,
        }


def award_upload_star(user_id: int, image_hash: str) -> bool:
    """Awards 1 star for a unique valid image upload. Prevents duplicate rewards."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR IGNORE INTO reward_events (user_id, reward_type, reference_id, stars_awarded)
                VALUES (?, 'upload', ?, 1);
                """,
                (user_id, image_hash),
            )
            awarded = cursor.rowcount > 0
            conn.commit()
            return awarded
    except Exception:
        return False


def award_quiz_rewards(
    user_id: int, category: str, chapter_id: int, score: int, max_questions: int = 5
) -> int:
    """Records quiz attempt, unlocks next chapter if score >= 3, and awards non-duplicate stars.
    Returns total new stars awarded in this attempt.
    """
    new_stars = 0
    with get_connection() as conn:
        cursor = conn.cursor()

        # Record attempt
        cursor.execute(
            """
            INSERT INTO quiz_attempts (user_id, category, chapter_id, score)
            VALUES (?, ?, ?, ?);
            """,
            (user_id, category.lower(), chapter_id, score),
        )

        # Update chapter progress
        cursor.execute(
            """
            SELECT best_score, is_unlocked, is_completed FROM chapter_progress
            WHERE user_id = ? AND category = ? AND chapter_id = ?;
            """,
            (user_id, category.lower(), chapter_id),
        )
        prog = cursor.fetchone()
        current_best = prog["best_score"] if prog else 0

        is_passed = score >= 3
        new_best = max(current_best, score)

        cursor.execute(
            """
            INSERT INTO chapter_progress (user_id, category, chapter_id, best_score, is_unlocked, is_completed)
            VALUES (?, ?, ?, ?, 1, ?)
            ON CONFLICT(user_id, category, chapter_id) DO UPDATE SET
                best_score = MAX(best_score, excluded.best_score),
                is_completed = CASE WHEN excluded.is_completed = 1 THEN 1 ELSE is_completed END;
            """,
            (user_id, category.lower(), chapter_id, new_best, 1 if is_passed else 0),
        )

        # Unlock next chapter if passed
        if is_passed and chapter_id < 3:
            cursor.execute(
                """
                INSERT INTO chapter_progress (user_id, category, chapter_id, best_score, is_unlocked, is_completed)
                VALUES (?, ?, ?, 0, 1, 0)
                ON CONFLICT(user_id, category, chapter_id) DO UPDATE SET
                    is_unlocked = 1;
                """,
                (user_id, category.lower(), chapter_id + 1),
            )

        # Award question-level stars for new correct answers
        # For each correct score, award star if score exceeds previous best
        for q_idx in range(1, score + 1):
            ref_id = f"{category.lower()}_{chapter_id}_q{q_idx}"
            cursor.execute(
                """
                INSERT OR IGNORE INTO reward_events (user_id, reward_type, reference_id, stars_awarded)
                VALUES (?, 'quiz_question', ?, 1);
                """,
                (user_id, ref_id),
            )
            if cursor.rowcount > 0:
                new_stars += 1

        # Perfect score bonus (5/5): +3 stars once per chapter
        if score == max_questions:
            ref_perfect = f"perfect_{category.lower()}_{chapter_id}"
            cursor.execute(
                """
                INSERT OR IGNORE INTO reward_events (user_id, reward_type, reference_id, stars_awarded)
                VALUES (?, 'perfect_bonus', ?, 3);
                """,
                (user_id, ref_perfect),
            )
            if cursor.rowcount > 0:
                new_stars += 3

        conn.commit()

    return new_stars


def get_chapter_progress(user_id: int, category: str) -> Dict[int, Dict[str, Any]]:
    """Fetches unlock and completion status for all 3 chapters in a category."""
    progress = {}
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT chapter_id, best_score, is_unlocked, is_completed
            FROM chapter_progress
            WHERE user_id = ? AND category = ?;
            """,
            (user_id, category.lower()),
        )
        rows = cursor.fetchall()
        for r in rows:
            progress[r["chapter_id"]] = {
                "best_score": r["best_score"],
                "is_unlocked": bool(r["is_unlocked"]),
                "is_completed": bool(r["is_completed"]),
            }

    # Default fallback: Chapter 1 is always unlocked
    if 1 not in progress:
        progress[1] = {"best_score": 0, "is_unlocked": True, "is_completed": False}
    for ch in [2, 3]:
        if ch not in progress:
            progress[ch] = {"best_score": 0, "is_unlocked": False, "is_completed": False}

    return progress
