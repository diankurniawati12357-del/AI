"""Unit tests for BIOVA Classification & Model Services."""

import unittest
import io
from PIL import Image
from services.upload_service import validate_and_process_upload
from services.model_service import check_model_availability, classify_image
from services.edukasi_service import get_education_info
from services.model3d_service import get_model3d_info


class DummyUpload:
    def __init__(self, name: str, bytes_data: bytes):
        self.name = name
        self._bytes = bytes_data

    def getvalue(self) -> bytes:
        return self._bytes


class TestClassificationService(unittest.TestCase):
    def test_upload_validation_valid_png(self):
        # Create a valid test image
        img = Image.new("RGB", (100, 100), color=(100, 150, 200))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        dummy = DummyUpload("test_photo.png", buf.getvalue())

        is_valid, msg, loaded_img, img_hash = validate_and_process_upload(dummy)
        self.assertTrue(is_valid)
        self.assertIsNotNone(loaded_img)
        self.assertEqual(len(img_hash), 64)  # SHA-256 hex string

    def test_upload_validation_invalid_extension(self):
        dummy = DummyUpload("script.exe", b"fake binary content")
        is_valid, msg, _, _ = validate_and_process_upload(dummy)
        self.assertFalse(is_valid)
        self.assertIn("tidak didukung", msg.lower())

    def test_upload_validation_corrupted_image(self):
        dummy = DummyUpload("corrupted.jpg", b"corrupted non image bytes")
        is_valid, msg, _, _ = validate_and_process_upload(dummy)
        self.assertFalse(is_valid)
        self.assertIn("rusak", msg.lower())

    def test_model_availability_check(self):
        # When models/model_hewan.keras does not exist, should report model_unavailable cleanly
        is_ready, msg = check_model_availability("hewan")
        # In initial state, model file has not been trained/placed yet
        self.assertFalse(is_ready)
        self.assertIn("model ai belum tersedia", msg.lower())

    def test_classification_with_missing_model_returns_graceful_status(self):
        img = Image.new("RGB", (224, 224), color=(50, 100, 150))
        res = classify_image("hewan", img)
        self.assertEqual(res["status"], "model_unavailable")
        self.assertIn("model ai belum tersedia", res["message"].lower())

    def test_species_catalog_resolution(self):
        mamalia_info = get_education_info("hewan", "Mamalia")
        self.assertIsNotNone(mamalia_info)
        self.assertIn("menyusui", mamalia_info["description"].lower())

        dikotil_info = get_education_info("tumbuhan", "Dikotil")
        self.assertIsNotNone(dikotil_info)
        self.assertIn("dua keping biji", dikotil_info["description"].lower())

    def test_3d_model_mapping_fallback(self):
        info = get_model3d_info("hewan", "Mamalia")
        # Check whether physical model exists or gracefully handles absence
        self.assertIn("exists", info)
        self.assertIn("filename", info)
        if not info["exists"]:
            self.assertIsNone(info["model_path"])


if __name__ == "__main__":
    unittest.main()
