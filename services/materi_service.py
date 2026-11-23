"""BIOVA Material Service
Loads and parses structured educational lessons for animals and plants.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from services.config import CONTENT_DIR


def load_material_data(category: str) -> Dict[str, Any]:
    """Loads material JSON data for the given category ('hewan' or 'tumbuhan')."""
    file_map = {
        "hewan": CONTENT_DIR / "materi_hewan.json",
        "tumbuhan": CONTENT_DIR / "materi_tumbuhan.json",
    }
    path = file_map.get(category.lower())
    if not path or not path.exists():
        return {"chapters": []}

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"chapters": []}


def get_all_chapters(category: str) -> List[Dict[str, Any]]:
    """Returns legacy chapter records for compatibility with existing content."""
    data = load_material_data(category)
    return data.get("chapters", [])


def get_all_cards(category: str) -> List[Dict[str, Any]]:
    """Returns the active, chapter-free material collection for a category."""
    chapters = get_all_chapters(category)
    if not chapters:
        return []

    cards = []
    for index, card in enumerate(chapters[0].get("cards", []), start=1):
        material = dict(card)
        material["material_id"] = str(
            card.get("class_id") or card.get("topic_id") or f"{category}-{index}"
        )
        cards.append(material)
    return cards


def get_chapter_by_id(category: str, chapter_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves a legacy chapter record by ID."""
    chapters = get_all_chapters(category)
    for ch in chapters:
        if ch["id"] == chapter_id:
            return ch
    return None


def get_card(category: str, chapter_id: int, card_index: int) -> Optional[Dict[str, Any]]:
    """Retrieves a legacy educational card within a chapter by 0-based index."""
    ch = get_chapter_by_id(category, chapter_id)
    if not ch:
        return None
    cards = ch.get("cards", [])
    if 0 <= card_index < len(cards):
        return cards[card_index]
    return None
