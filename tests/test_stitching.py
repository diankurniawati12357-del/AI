"""Unit tests for BIOVA Image Stitching Service."""

import unittest
from PIL import Image, ImageDraw
from services.stitching_service import stitch_images, get_image_download_bytes


class TestStitchingService(unittest.TestCase):
    def test_stitching_requires_at_least_two_images(self):
        img1 = Image.new("RGB", (200, 200), color=(100, 100, 100))
        success, res, msg = stitch_images([img1])
        self.assertFalse(success)
        self.assertIsNone(res)
        self.assertIn("minimal 2 foto", msg.lower())

    def test_stitching_non_overlapping_images_fails_gracefully(self):
        # Two completely blank images with different solid colors have zero feature matches
        img1 = Image.new("RGB", (300, 300), color=(255, 0, 0))
        img2 = Image.new("RGB", (300, 300), color=(0, 0, 255))

        success, res, msg = stitch_images([img1, img2])
        self.assertFalse(success)
        self.assertIsNone(res)
        self.assertTrue(len(msg) > 0)

    def test_download_bytes_generation(self):
        img = Image.new("RGB", (100, 100), color=(200, 220, 240))
        raw_bytes = get_image_download_bytes(img, format="JPEG")
        self.assertGreater(len(raw_bytes), 0)
        # JPEG header starts with \xff\xd8
        self.assertTrue(raw_bytes.startswith(b"\xff\xd8"))


if __name__ == "__main__":
    unittest.main()
