"""Unit tests for BIOVA Learning & Quiz Services."""

import unittest
from services.materi_service import get_all_chapters, get_chapter_by_id, get_card
from services.quiz_service import get_questions, check_answer


class TestQuizAndLearningService(unittest.TestCase):
    def test_material_chapters_structure(self):
        # Animal chapters
        hewan_chapters = get_all_chapters("hewan")
        self.assertEqual(len(hewan_chapters), 3, "Animal category must have exactly 3 chapters")
        for ch in hewan_chapters:
            self.assertEqual(len(ch.get("cards", [])), 5, f"Chapter {ch['id']} must have 5 cards")

        # Plant chapters
        tumbuhan_chapters = get_all_chapters("tumbuhan")
        self.assertEqual(len(tumbuhan_chapters), 3, "Plant category must have exactly 3 chapters")
        for ch in tumbuhan_chapters:
            self.assertEqual(len(ch.get("cards", [])), 5, f"Chapter {ch['id']} must have 5 cards")

    def test_get_specific_card(self):
        card = get_card("hewan", chapter_id=1, card_index=0)
        self.assertIsNotNone(card)
        self.assertIn("Mamalia", card["title"])

    def test_quiz_questions_structure(self):
        for cat in ["hewan", "tumbuhan"]:
            for ch_id in [1, 2, 3]:
                questions = get_questions(cat, ch_id)
                self.assertEqual(len(questions), 5, f"{cat} chapter {ch_id} must have 5 questions")
                for q in questions:
                    self.assertTrue(len(q["question"]) > 5)
                    self.assertEqual(len(q["options"]), 4, "Each question must have 4 options")
                    self.assertIn(q["correct_answer"], q["options"], "Correct answer must be among options")
                    self.assertTrue(len(q["explanation"]) > 10, "Explanation must be thorough")

    def test_check_answer_accuracy(self):
        # Check answer for animal chapter 2 question 1 (Herbivora)
        questions = get_questions("hewan", chapter_id=2)
        q1 = questions[0]
        correct_ans = q1["correct_answer"]

        # Test correct answer
        is_correct, ans, expl = check_answer("hewan", chapter_id=2, question_index=0, user_answer=correct_ans)
        self.assertTrue(is_correct)
        self.assertEqual(ans, correct_ans)
        self.assertTrue(len(expl) > 0)

        # Test incorrect answer
        wrong_ans = [o for o in q1["options"] if o != correct_ans][0]
        is_wrong, ans2, _ = check_answer("hewan", chapter_id=2, question_index=0, user_answer=wrong_ans)
        self.assertFalse(is_wrong)
        self.assertEqual(ans2, correct_ans)


if __name__ == "__main__":
    unittest.main()
