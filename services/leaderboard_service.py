"""BIOVA Leaderboard Service
Retrieves live leaderboard rankings from SQLite database without hardcoded fake data.
"""

from typing import List, Dict, Any, Optional
from services.db import get_connection
from services.game_service import calculate_tier


def get_leaderboard(limit: int = 50) -> List[Dict[str, Any]]:
    """Fetches real leaderboard rankings sorted by stars and earliest registration date."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 
                u.id,
                u.username,
                COALESCE(SUM(r.stars_awarded), 0) AS total_stars,
                (SELECT COUNT(*) FROM reward_events re WHERE re.user_id = u.id AND re.reward_type = 'upload') AS upload_count,
                u.created_at
            FROM users u
            LEFT JOIN reward_events r ON u.id = r.user_id
            GROUP BY u.id
            ORDER BY total_stars DESC, u.created_at ASC
            LIMIT ?;
            """,
            (limit,),
        )
        rows = cursor.fetchall()

        leaderboard = []
        for rank, row in enumerate(rows, start=1):
            tier = calculate_tier(row["total_stars"], row["upload_count"])
            leaderboard.append({
                "rank": rank,
                "user_id": row["id"],
                "username": row["username"],
                "stars": row["total_stars"],
                "tier": tier["name"],
                "tier_icon": tier["icon"],
            })
        return leaderboard


def get_user_rank(user_id: int) -> Optional[int]:
    """Computes the exact rank position of a given user."""
    board = get_leaderboard(limit=1000)
    for entry in board:
        if entry["user_id"] == user_id:
            return entry["rank"]
    return None
