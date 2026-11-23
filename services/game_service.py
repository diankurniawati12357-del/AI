"""BIOVA Gamification & Progress Service
Manages star calculation, material completion, and one-time quiz rewards.
"""

from typing import Tuple, Dict, Any, List, Optional
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

        cursor.execute(
            "SELECT COUNT(*) AS completed_material FROM material_progress "
            "WHERE user_id = ? AND is_completed = 1;",
            (user_id,),
        )
        completed_material = cursor.fetchone()["completed_material"]

        tier_info = calculate_tier(stars, upload_count)

        return {
            "stars": stars,
            "tier": tier_info["name"],
            "tier_icon": tier_info["icon"],
            "tier_color": tier_info["color"],
            "stars_needed": tier_info["stars_needed"],
            "upload_count": upload_count,
            "quiz_count": quiz_count,
            "completed_material": completed_material,
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
    user_id: int,
    category: str,
    chapter_id: int = 1,
    score: int = 0,
    max_questions: int = 5,
    question_ids: Optional[List[str]] = None,
) -> int:
    """Records an attempt and awards one-time stars for correct bank question IDs.

    The legacy chapter_id parameter remains accepted for older callers and quiz_attempts rows.
    """
    category = category.lower()
    score = max(0, min(int(score), max_questions))
    legacy_rewards = question_ids is None
    if legacy_rewards:
        question_ids = [str(index) for index in range(1, score + 1)]
        perfect_reference = f"perfect_{category}_{chapter_id}"
    else:
        question_ids = list(dict.fromkeys(str(question_id) for question_id in question_ids))[:score]
        score = len(question_ids)
        perfect_reference = f"perfect_bank-v2_{category}"

    new_stars = 0
    with get_connection() as conn:
        cursor = conn.cursor()

        # Record attempt
        cursor.execute(
            """
            INSERT INTO quiz_attempts (user_id, category, chapter_id, score)
            VALUES (?, ?, ?, ?);
            """,
            (user_id, category, 1, score),
        )

        for question_id in question_ids:
            ref_id = (
                f"{category}_{chapter_id}_q{question_id}"
                if legacy_rewards
                else f"bank-v2_{category}_{question_id}"
            )
            cursor.execute(
                """
                INSERT OR IGNORE INTO reward_events (user_id, reward_type, reference_id, stars_awarded)
                VALUES (?, 'quiz_question', ?, 1);
                """,
                (user_id, ref_id),
            )
            if cursor.rowcount > 0:
                new_stars += 1

        if score == max_questions:
            cursor.execute(
                """
                INSERT OR IGNORE INTO reward_events (user_id, reward_type, reference_id, stars_awarded)
                VALUES (?, 'perfect_bonus', ?, 3);
                """,
                (user_id, perfect_reference),
            )
            if cursor.rowcount > 0:
                new_stars += 3

        conn.commit()

    return new_stars


def get_material_progress(user_id: int, category: str) -> set:
    """Returns IDs of completed materials without changing legacy chapter progress."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT material_id FROM material_progress
            WHERE user_id = ? AND category = ? AND is_completed = 1;
            """,
            (user_id, category.lower()),
        ).fetchall()
    return {str(row["material_id"]) for row in rows}


def mark_material_completed(user_id: int, category: str, material_id: str) -> bool:
    """Persists completion of one material idempotently."""
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT OR IGNORE INTO material_progress (user_id, category, material_id, is_completed)
            VALUES (?, ?, ?, 1);
            """,
            (user_id, category.lower(), material_id),
        )
        conn.commit()
        return cursor.rowcount > 0


def get_chapter_progress(user_id: int, category: str) -> Dict[int, Dict[str, Any]]:
    """Reads preserved legacy chapter progress; active UI uses material progress."""
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
