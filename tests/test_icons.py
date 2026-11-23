import base64
import unittest
from pathlib import Path

from components.icons import (
    get_icon_base64,
    get_icon_path,
    render_icon,
    normalize_animal_class,
    get_animal_class_icon,
    get_plant_topic_icon,
)


ICON_DIR = Path(__file__).resolve().parent.parent / "icon"


class TestIconManager(unittest.TestCase):
    def test_animal_class_icon_mapping(self):
        expected = {
            "mamalia": "icon_mamalia.png",
            "aves": "icon_aves.png",
            "reptilia": "icon_reptilia.png",
            "amfibi": "icon_amfibi.png",
            "pisces": "icon_pisces.png",
            "invertebrata": "icon_invertebrata.png",
        }
        for class_id, icon_name in expected.items():
            with self.subTest(class_id=class_id):
                resolved, normalized = get_animal_class_icon(class_id)
                self.assertEqual(normalized, class_id)
                self.assertEqual(resolved, icon_name)

        resolved, normalized = get_animal_class_icon("Kelas: Mamalia")
        self.assertEqual(normalized, "mamalia")
        self.assertEqual(resolved, "icon_mamalia.png")
        resolved, normalized = get_animal_class_icon("Mamalia (Hewan Menyusui)")
        self.assertEqual(normalized, "mamalia")
        self.assertEqual(resolved, "icon_mamalia.png")

    def test_plant_topic_icon_mapping(self):
        expected = {
            "biji_keping": "icon_bijikeping.png",
            "sistem_perakaran": "icon_sistemperakaran.png",
            "tulang_daun": "icon_strukturtulangdaun.png",
            "batang_kambium": "icon_batangkambium.png",
            "struktur_bunga": "icon_strukturbunga.png",
        }
        for topic_id, icon_name in expected.items():
            with self.subTest(topic_id=topic_id):
                self.assertEqual(get_plant_topic_icon(topic_id), icon_name)
    def test_all_bundled_icon_files_resolve(self):
        icon_files = list(ICON_DIR.glob("icon_*.png"))
        self.assertTrue(icon_files)

        for icon_file in icon_files:
            with self.subTest(icon=icon_file.name):
                icon_name = icon_file.stem[len("icon_"):]
                self.assertEqual(get_icon_path(icon_name), icon_file)
                self.assertTrue(get_icon_base64(icon_name))

    def test_html_icons_use_embedded_png_data(self):
        rendered = render_icon("hewan", 56, "biova-icon--category", "Kategori hewan")

        self.assertIn('src="data:image/png;base64,', rendered)
        self.assertIn('alt="Kategori hewan"', rendered)
        self.assertIn('object-fit:contain', rendered)
        self.assertTrue(base64.b64decode(get_icon_base64("hewan")).startswith(b"\x89PNG"))

    def test_missing_icon_uses_non_broken_fallback(self):
        rendered = render_icon("not-a-real-icon", 24, alt="Ikon tidak tersedia")

        self.assertIn('class="biova-icon-fallback', rendered)
        self.assertNotIn("<img", rendered)
        self.assertIn('aria-label="Ikon tidak tersedia"', rendered)


if __name__ == "__main__":
    unittest.main()
