"""BIOVA Image Stitching Service
Combines multiple overlapping photos into a wide panorama using OpenCV Stitcher.
"""

import io
from typing import List, Tuple, Optional
import cv2
import numpy as np
from PIL import Image


def stitch_images(pil_images: List[Image.Image]) -> Tuple[bool, Optional[Image.Image], str]:
    """Stitches a list of PIL Images into a panoramic image using OpenCV.
    Returns: (success, stitched_pil_image, status_message).
    """
    if len(pil_images) < 2:
        return False, None, "Minimal 2 foto dengan area tumpang tindih (overlap) diperlukan untuk membuat panorama."

    cv2_images = []
    for img in pil_images:
        # Convert PIL to RGB then to OpenCV BGR
        rgb = np.array(img.convert("RGB"))
        bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

        # Downscale if image is overly large to conserve memory
        max_dim = 1400
        h, w = bgr.shape[:2]
        if max(h, w) > max_dim:
            scale = max_dim / float(max(h, w))
            bgr = cv2.resize(bgr, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)

        cv2_images.append(bgr)

    # Initialize OpenCV Stitcher
    try:
        # Try OpenCV Stitcher creation
        stitcher = cv2.Stitcher.create(cv2.Stitcher_PANORAMA)
        status, stitched = stitcher.stitch(cv2_images)

        if status == cv2.Stitcher_OK:
            # Convert stitched BGR back to PIL RGB
            stitched_rgb = cv2.cvtColor(stitched, cv2.COLOR_BGR2RGB)
            result_pil = Image.fromarray(stitched_rgb)
            return True, result_pil, "Foto berhasil digabungkan menjadi panorama!"
        elif status == cv2.Stitcher_ERR_NEED_MORE_IMGS:
            return False, None, "Jumlah foto atau area overlap tidak mencukupi untuk membuat panorama."
        elif status == cv2.Stitcher_ERR_HOMOGRAPHY_EST_FAIL:
            return (
                False,
                None,
                "Titik kecocokan (fitur visual) tidak cukup ditemukan di antara foto-foto ini. Pastikan foto memiliki bagian objek yang saling tumpang tindih minimal 30-50%.",
            )
        elif status == cv2.Stitcher_ERR_CAMERA_PARAMS_ADJUST_FAIL:
            return False, None, "Penyesuaian parameter kamera gagal. Coba gunakan foto dengan pencahayaan dan sudut serupa."
        else:
            return False, None, f"Penggabungan foto gagal (kode status OpenCV: {status})."

    except Exception as e:
        return False, None, f"Terjadi kesalahan saat memproses panorama: {str(e)}"


def get_image_download_bytes(img: Image.Image, format: str = "JPEG") -> bytes:
    """Converts a PIL image to bytes buffer for Streamlit download button."""
    buf = io.BytesIO()
    img.save(buf, format=format, quality=95)
    return buf.getvalue()
