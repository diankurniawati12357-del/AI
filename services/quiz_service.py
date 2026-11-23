"""BIOVA Quiz Service
Loads and grades interactive multiple-choice quiz questions and explanations.
"""

import json
import logging
import random
import uuid
from typing import Dict, Any, List, Optional, Tuple
from services.config import CONTENT_DIR

_LOGGER = logging.getLogger(__name__)

def load_quiz_data(category: str) -> Dict[str, Any]:
    """Loads the bilingual question bank for the given category."""
    file_map = {
        "hewan": CONTENT_DIR / "kuis_hewan.json",
        "tumbuhan": CONTENT_DIR / "kuis_tumbuhan.json",
    }
    path = file_map.get(category.lower())
    if not path or not path.exists():
        return {"questions": []}

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        _LOGGER.exception("Unable to load quiz bank for category %s", category)
        return {"questions": []}
    return data if isinstance(data, dict) else {"questions": []}


def _localized_pair_is_valid(value: Any) -> bool:
    return (
        isinstance(value, dict)
        and isinstance(value.get("id"), str)
        and bool(value["id"].strip())
        and isinstance(value.get("en"), str)
        and bool(value["en"].strip())
    )


def is_valid_question(question: Any) -> bool:
    """Checks the complete bilingual, stable-ID question contract."""
    if not isinstance(question, dict) or not str(question.get("id", "")).strip():
        return False
    if not str(question.get("topic", "")).strip():
        return False
    if not _localized_pair_is_valid(question.get("question")):
        return False
    if not _localized_pair_is_valid(question.get("explanation")):
        return False

    options = question.get("options")
    if not isinstance(options, dict) or len(options) != 3:
        return False
    option_ids = list(options)
    return (
        all(isinstance(option_id, str) for option_id in option_ids)
        and all(_localized_pair_is_valid(text) for text in options.values())
        and len(set(option_ids)) == 3
        and question.get("correct_option_id") in option_ids
    )


def get_questions(category: str) -> List[Dict[str, Any]]:
    """Returns all valid questions in a category question bank."""
    data = load_quiz_data(category)
    bank = data.get("questions", [])
    if not isinstance(bank, list):
        return []
    return [question for question in bank if is_valid_question(question)]


def get_question_by_id(category: str, question_id: str) -> Optional[Dict[str, Any]]:
    return next(
        (question for question in get_questions(category) if question["id"] == question_id),
        None,
    )


def create_quiz_session(
    category: str, question_count: int = 5, rng: Optional[random.Random] = None
) -> Dict[str, Any]:
    """Selects questions and option orders once, ready to persist in Streamlit session state."""
    questions = get_questions(category)
    if len(questions) < question_count:
        raise ValueError(
            f"Kuis {category} membutuhkan {question_count} soal valid; "
            f"hanya {len(questions)} yang tersedia."
        )

    chooser = rng or random
    selected = chooser.sample(questions, question_count)
    option_orders = {}
    for question in selected:
        option_ids = list(question["options"])
        option_orders[question["id"]] = chooser.sample(option_ids, len(option_ids))

    return {
        "session_id": uuid.uuid4().hex,
        "question_ids": [question["id"] for question in selected],
        "option_orders": option_orders,
        "answers": {},
        "checked_ids": [],
    }


def initialize_quiz_session(category: str, session_state: Any) -> bool:
    """Starts a fresh category-specific quiz session in the supplied session state."""
    category = category.lower()
    try:
        quiz_session = create_quiz_session(category)
    except ValueError as error:
        session_state["quiz_start_error"] = str(error)
        session_state["quiz_category"] = category
        sessions = dict(session_state.get("quiz_sessions", {}))
        sessions.pop(category, None)
        session_state["quiz_sessions"] = sessions
        return False

    sessions = dict(session_state.get("quiz_sessions", {}))
    sessions[category] = quiz_session
    session_state["quiz_sessions"] = sessions
    session_state["quiz_category"] = category
    session_state["learning_category"] = category
    session_state["quiz_q_index"] = 0
    session_state.pop("quiz_start_error", None)
    return True


def check_answer(
    category: str, question_id: str, user_option_id: str
) -> Tuple[bool, str, Dict[str, str]]:
    """Grades by stable option ID and returns correctness, correct ID, and bilingual feedback."""
    question = get_question_by_id(category, question_id)
    if not question:
        return False, "", {"id": "Pertanyaan tidak ditemukan.", "en": "Question not found."}
    correct = question["correct_option_id"]
    return user_option_id == correct, correct, question["explanation"]
