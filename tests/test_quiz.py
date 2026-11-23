"""Tests for chapter-free material collections and randomized bilingual quiz banks."""

import random
import unittest
from collections import Counter
from unittest.mock import patch

from components.i18n import localize_material_card, localize_quiz_question
from services.materi_service import get_all_cards
from services.quiz_service import (
    check_answer,
    create_quiz_session,
    get_questions,
    initialize_quiz_session,
    is_valid_question,
)


class TestQuizAndLearningService(unittest.TestCase):
    def test_material_collections_are_flat_and_complete(self):
        animal_cards = get_all_cards("hewan")
        plant_cards = get_all_cards("tumbuhan")
        self.assertEqual(len(animal_cards), 6)
        self.assertEqual(len(plant_cards), 5)
        self.assertEqual(
            [card["material_id"] for card in animal_cards],
            ["mamalia", "aves", "reptilia", "amfibi", "pisces", "invertebrata"],
        )
        self.assertEqual(
            [card["material_id"] for card in plant_cards],
            ["biji_keping", "sistem_perakaran", "tulang_daun", "batang_kambium", "struktur_bunga"],
        )

    def test_material_cards_have_complete_english_localizations(self):
        for category in ("hewan", "tumbuhan"):
            for card in get_all_cards(category):
                with patch("components.i18n.init_language", return_value="en"):
                    localized = localize_material_card(card)
                self.assertNotEqual(localized["title"], card["title"])
                self.assertNotEqual(localized["description"], card["description"])
                self.assertNotEqual(localized["characteristics"], card["characteristics"])

    def test_question_banks_are_valid_bilingual_and_balanced(self):
        expected_topics = {
            "hewan": {
                "mamalia": 5,
                "aves": 5,
                "reptilia": 5,
                "amfibi": 5,
                "pisces": 5,
                "invertebrata": 5,
            },
            "tumbuhan": {
                "biji_keping": 6,
                "sistem_perakaran": 6,
                "tulang_daun": 6,
                "batang_kambium": 6,
                "struktur_bunga": 6,
            },
        }
        for category, expected in expected_topics.items():
            questions = get_questions(category)
            self.assertEqual(len(questions), 30)
            self.assertEqual(len({question["id"] for question in questions}), 30)
            self.assertEqual(Counter(question["topic"] for question in questions), expected)
            for question in questions:
                self.assertTrue(is_valid_question(question))
                self.assertEqual(len(question["options"]), 3)
                self.assertIn(question["correct_option_id"], question["options"])
                self.assertTrue(all(option["id"] and option["en"] for option in question["options"].values()))

    def test_session_samples_five_unique_questions_and_shuffles_choices(self):
        for category in ("hewan", "tumbuhan"):
            session = create_quiz_session(category, rng=random.Random(12))
            self.assertEqual(len(session["question_ids"]), 5)
            self.assertEqual(len(set(session["question_ids"])), 5)
            for question_id in session["question_ids"]:
                question = next(q for q in get_questions(category) if q["id"] == question_id)
                self.assertEqual(
                    set(session["option_orders"][question_id]),
                    set(question["options"]),
                )
                self.assertEqual(len(session["option_orders"][question_id]), 3)

    def test_answer_grading_uses_option_id_not_display_position(self):
        question = get_questions("hewan")[0]
        correct_id = question["correct_option_id"]
        correct, returned_id, explanation = check_answer("hewan", question["id"], correct_id)
        self.assertTrue(correct)
        self.assertEqual(returned_id, correct_id)
        self.assertTrue(explanation["id"])
        self.assertTrue(explanation["en"])

        wrong_id = next(option_id for option_id in question["options"] if option_id != correct_id)
        incorrect, returned_id, _ = check_answer("hewan", question["id"], wrong_id)
        self.assertFalse(incorrect)
        self.assertEqual(returned_id, correct_id)

    def test_category_sessions_are_independent_and_language_does_not_change_ids(self):
        session_state = {}
        self.assertTrue(initialize_quiz_session("hewan", session_state))
        animal_session = session_state["quiz_sessions"]["hewan"]
        self.assertTrue(initialize_quiz_session("tumbuhan", session_state))
        plant_session = session_state["quiz_sessions"]["tumbuhan"]
        self.assertEqual(session_state["quiz_sessions"]["hewan"], animal_session)

        question = next(q for q in get_questions("hewan") if q["id"] == animal_session["question_ids"][0])
        for language in ("id", "en"):
            with patch("components.i18n.init_language", return_value=language):
                localize_quiz_question(question)
            self.assertEqual(session_state["quiz_sessions"]["hewan"]["question_ids"], animal_session["question_ids"])
            self.assertEqual(session_state["quiz_sessions"]["hewan"]["option_orders"], animal_session["option_orders"])
        self.assertNotEqual(animal_session["session_id"], plant_session["session_id"])

    def test_bank_with_fewer_than_five_valid_questions_fails_clearly(self):
        with patch("services.quiz_service.get_questions", return_value=[{}] * 4):
            with self.assertRaisesRegex(ValueError, "hanya 4"):
                create_quiz_session("hewan")

    def test_invalid_question_contract_is_rejected(self):
        self.assertFalse(is_valid_question({"id": "bad", "options": {"A": {}, "B": {}}}))


if __name__ == "__main__":
    unittest.main()
