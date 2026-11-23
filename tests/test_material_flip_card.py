import unittest
from unittest.mock import patch

from components.i18n import (
    COLLECTION_FLIP_COPY,
    EN,
    ID,
    MATERIAL_FLIP_COPY,
    get_collection_flip_copy,
    get_material_flip_copy,
)
from components.material_flip_card import build_material_flip_card_html


class TestMaterialFlipCard(unittest.TestCase):
    def test_all_material_copy_is_bilingual_and_keyed_by_stable_ids(self):
        expected_counts = {"hewan": 6, "tumbuhan": 5}
        for category, expected_count in expected_counts.items():
            self.assertEqual(len(MATERIAL_FLIP_COPY[category]), expected_count)
            for material_id in MATERIAL_FLIP_COPY[category]:
                for language in ("id", "en"):
                    with self.subTest(category=category, material_id=material_id, language=language):
                        with patch("components.i18n.init_language", return_value=language):
                            copy = get_material_flip_copy(category, material_id)
                        self.assertTrue(all(copy.values()))

    def test_flip_card_contains_3d_interaction_and_bilingual_copy(self):
        with patch("components.i18n.init_language", return_value="id"):
            copy = get_material_flip_copy("hewan", "mamalia")
        rendered = build_material_flip_card_html(
            icon_html='<img src="data:image/png;base64,abc" alt="Mamalia">',
            card_number="#01",
            title="Mamalia",
            category_label="Kelas: Mamalia",
            collection_label=ID["lesson.collection_brand"],
            number_label=ID["lesson.card_number"],
            flip_to_back_label=ID["lesson.flip_to_back"],
            flip_to_front_label=ID["lesson.flip_to_front"],
            did_you_know_label=ID["lesson.did_you_know"],
            fun_fact_label=ID["lesson.fun_fact"],
            examples_label=ID["lesson.examples"],
            theme="animals",
            language="id",
            **copy,
        )

        self.assertIn("perspective:1000px", rendered)
        self.assertIn("transform-style:preserve-3d", rendered)
        self.assertIn("backface-visibility:hidden", rendered)
        self.assertIn("transition:transform 650ms cubic-bezier(0.22, 1, 0.36, 1)", rendered)
        self.assertIn("transform:rotateY(180deg)", rendered)
        self.assertIn("font-family:\"Nunito Sans\"", rendered)
        self.assertIn(
            "background:linear-gradient(145deg,#143D2A 0%,#204D36 55%,#173E2B 100%)",
            rendered,
        )
        self.assertIn("Balik Kartu", rendered)
        self.assertIn("Balik Kembali", rendered)
        self.assertIn("Mamalia", rendered)
        self.assertIn("section-divider", rendered)
        self.assertIn("fun-fact-label", rendered)
        self.assertIn("background:rgba(255,255,255,.08)", rendered)
        self.assertIn("M61 35q4-9 16-9h18", rendered)
        self.assertIn("height:460px", rendered)
        self.assertIn("border:1px solid rgba(247,212,92,.5)", rendered)
        self.assertIn('card.classList.toggle("is-flipped", flipped)', rendered)
        self.assertIn("Mamalia adalah hewan yang menyusui anaknya.", rendered)
        self.assertIn("Kancil juga termasuk mamalia", rendered)
        self.assertIn("Kancil, gajah, kucing.", rendered)
        self.assertIn("CARD #01", rendered)

    def test_card_text_is_escaped_before_embedding(self):
        rendered = build_material_flip_card_html(
            icon_html="<img>",
            card_number="#01",
            title="<script>alert(1)</script>",
            category_label="Class",
            description="Description",
            fun_fact="Fact",
            examples="Examples",
            collection_label="Collection",
            number_label="Card",
            flip_to_back_label="Flip",
            flip_to_front_label="Return",
            did_you_know_label="Did you know?",
            fun_fact_label="Fun fact",
            examples_label="Examples",
            theme="plants",
            language="en",
        )

        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", rendered)
        self.assertNotIn("<h1><script>", rendered)
        self.assertIn("M90 45V23", rendered)

    def test_english_controls_and_back_heading_render_from_active_translations(self):
        rendered = build_material_flip_card_html(
            icon_html="<img>",
            card_number="#01",
            title="Mammals",
            category_label="Class: Mammals",
            description="Animals that nurse their young.",
            fun_fact="Bats are mammals that can fly!",
            examples="Mouse-deer, cats, elephants.",
            collection_label=EN["lesson.collection_brand"],
            number_label=EN["lesson.card_number"],
            flip_to_back_label=EN["lesson.flip_to_back"],
            flip_to_front_label=EN["lesson.flip_to_front"],
            did_you_know_label=EN["lesson.did_you_know"],
            fun_fact_label=EN["lesson.fun_fact"],
            examples_label=EN["lesson.examples"],
            theme="animals",
            language="en",
        )

        self.assertIn("BIOVA NATURE COLLECTION", rendered)
        self.assertIn("CARD #01", rendered)
        self.assertIn("Mammals", rendered)
        self.assertIn("section-divider", rendered)
        self.assertIn("Flip Card", rendered)
        self.assertIn("Tap to return", rendered)
        self.assertIn("Examples", rendered)

    def test_collection_copy_covers_all_stable_ids_in_both_languages(self):
        expected_counts = {"hewan": 6, "tumbuhan": 5}
        for category, expected_count in expected_counts.items():
            self.assertEqual(len(COLLECTION_FLIP_COPY[category]), expected_count)
            for material_id in COLLECTION_FLIP_COPY[category]:
                for language in ("id", "en"):
                    with self.subTest(category=category, material_id=material_id, language=language):
                        with patch("components.i18n.init_language", return_value=language):
                            copy = get_collection_flip_copy(category, material_id)
                        self.assertTrue(all(copy.values()))

    def test_collection_card_uses_shared_3d_flip_and_persistent_per_card_state(self):
        with patch("components.i18n.init_language", return_value="id"):
            copy = get_collection_flip_copy("hewan", "mamalia")
        rendered = build_material_flip_card_html(
            icon_html='<img src="data:image/png;base64,abc" alt="Mamalia">',
            card_number="#01",
            title="Mamalia",
            category_label="Kelas: Mamalia",
            collection_label=ID["lesson.collection_brand"],
            number_label=ID["lesson.card_number"],
            flip_to_back_label=ID["lesson.flip_to_back"],
            flip_to_front_label=ID["collection.return"],
            did_you_know_label=ID["lesson.did_you_know"],
            fun_fact_label=ID["lesson.fun_fact"],
            examples_label=ID["lesson.examples"],
            theme="animals",
            language="id",
            front_description="Mamalia menyusui anaknya.",
            overview_label=ID["collection.overview"],
            flip_indicator_label="Balik Kartu",
            state_key="animal_mamalia",
            mode="collection",
            **copy,
        )

        self.assertIn("transition:transform 650ms cubic-bezier(0.22, 1, 0.36, 1)", rendered)
        self.assertIn(
            "background:linear-gradient(145deg,#143D2A 0%,#204D36 55%,#173E2B 100%)",
            rendered,
        )
        self.assertIn("Balik Kartu", rendered)
        self.assertIn("Balik Kembali", rendered)
        self.assertIn("Ringkasan", rendered)
        self.assertIn("Fakta Menarik", rendered)
        self.assertIn("Mamalia menyusui anaknya.", rendered)
        self.assertIn("Hewan yang menyusui anaknya", rendered)
        self.assertIn("Kancil dan kelelawar sama-sama mamalia", rendered)
        self.assertIn("animal_mamalia", rendered)
        self.assertIn('window.localStorage.getItem(storageKey)', rendered)
        self.assertIn('window.localStorage.setItem(storageKey', rendered)
        self.assertIn('card.classList.toggle("is-flipped", flipped)', rendered)


if __name__ == "__main__":
    unittest.main()
