"""BIOVA Quiz Service
Loads and grades interactive multiple-choice quiz questions and explanations.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from services.config import CONTENT_DIR


def load_quiz_data(category: str) -> Dict[str, Any]:
    """Loads quiz JSON data for the given category ('hewan' or 'tumbuhan')."""
    file_map = {
        "hewan": CONTENT_DIR / "kuis_hewan.json",
        "tumbuhan": CONTENT_DIR / "kuis_tumbuhan.json",
    }
    path = file_map.get(category.lower())
    if not path or not path.exists():
        return {"chapters": []}

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"chapters": []}


def get_quiz_chapter(category: str, chapter_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves quiz questions for a specific chapter."""
    data = load_quiz_data(category)
    for ch in data.get("chapters", []):
        if ch["id"] == chapter_id:
            return ch
    return None


def get_questions(category: str, chapter_id: int) -> List[Dict[str, Any]]:
    """Retrieves the list of 5 questions for a chapter."""
    ch = get_quiz_chapter(category, chapter_id)
    return ch.get("questions", []) if ch else []


def check_answer(
    category: str, chapter_id: int, question_index: int, user_answer: str
) -> Tuple[bool, str, str]:
    """Grades user answer against the correct answer and returns (is_correct, correct_answer, explanation)."""
    questions = get_questions(category, chapter_id)
    if not (0 <= question_index < len(questions)):
        return False, "", "Pertanyaan tidak ditemukan."

    q = questions[question_index]
    correct = q.get("correct_answer", "").strip()
    is_correct = user_answer.strip().lower() == correct.lower()
    explanation = q.get("explanation", "")

    return is_correct, correct, explanation
