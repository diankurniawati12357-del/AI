"""BIOVA Image Upload Service
Validates uploaded image files (type, size, integrity) and computes unique hashes.
"""

import hashlib
import io
from typing import Tuple, Optional
from PIL import Image

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


def validate_and_process_upload(uploaded_file) -> Tuple[bool, str, Optional[Image.Image], str]:
    """Validates an uploaded image and decodes it safely with PIL.
    Returns: (is_valid, message, PIL.Image or None, sha256_hash).
    """
    if uploaded_file is None:
        return False, "Tidak ada file yang diunggah.", None, ""

    # Check extension
    filename = uploaded_file.name.lower()
    ext = filename.rsplit(".", 1)[-1] if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Format file .{ext} tidak didukung. Harap unggah file JPG, JPEG, atau PNG.", None, ""

    # Check file size
    bytes_data = uploaded_file.getvalue()
    if len(bytes_data) > MAX_FILE_SIZE_BYTES:
        return False, "Ukuran file melebihi batas maksimum 10 MB.", None, ""

    # Compute SHA-256 hash for anti-duplication tracking
    img_hash = hashlib.sha256(bytes_data).hexdigest()

    # Verify image integrity using Pillow
    try:
        img = Image.open(io.BytesIO(bytes_data))
        img.verify()  # Fast structural verification
        # Reopen because verify() closes the file pointer
        img = Image.open(io.BytesIO(bytes_data))
        img.load()  # Full image decode into memory
        
        # Verify reasonable resolution
        if img.width < 32 or img.height < 32:
            return False, "Resolusi gambar terlalu kecil (minimal 32x32 piksel).", None, ""

        return True, "Validasi gambar berhasil.", img, img_hash
    except Exception as e:
        return False, f"File gambar rusak atau tidak dapat diproses: {str(e)}", None, ""
