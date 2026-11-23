"""Persistent local profile photo storage and validation."""

import io
import os
import uuid
from pathlib import Path

from PIL import Image, ImageOps

from services.db import get_connection
from services.config import DATA_DIR


PROFILE_DIR = DATA_DIR / "profile_photos"
PROFILE_DIR.mkdir(parents=True, exist_ok=True)
MAX_PROFILE_SIZE = 5 * 1024 * 1024
ALLOWED_PROFILE_TYPES = {"image/jpeg", "image/png", "image/webp"}


def get_profile_photo_path(user_id: int):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT profile_photo_path FROM users WHERE id = ?;", (user_id,)
        ).fetchone()
    if not row or not row["profile_photo_path"]:
        return None
    path = Path(row["profile_photo_path"])
    return path if path.is_file() else None


def validate_and_save_profile_photo(user_id: int, uploaded_file) -> tuple[bool, str, Path | None]:
    mime_type = getattr(uploaded_file, "type", "") or ""
    if mime_type and mime_type not in ALLOWED_PROFILE_TYPES:
        return False, "Format foto profil harus JPG, JPEG, PNG, atau WEBP.", None
    try:
        contents = uploaded_file.getvalue()
    except Exception:
        return False, "Gambar profil tidak dapat dibaca.", None

    if not contents:
        return False, "Gambar profil tidak boleh kosong.", None
    if len(contents) > MAX_PROFILE_SIZE:
        return False, "Ukuran foto profil maksimal 5 MB.", None

    try:
        with Image.open(io.BytesIO(contents)) as image:
            image.verify()
        with Image.open(io.BytesIO(contents)) as image:
            image = ImageOps.exif_transpose(image).convert("RGBA")
            if image.width < 32 or image.height < 32:
                return False, "Resolusi foto profil terlalu kecil.", None
            size = min(image.width, image.height)
            left = (image.width - size) // 2
            top = (image.height - size) // 2
            image = image.crop((left, top, left + size, top + size)).resize((256, 256), Image.Resampling.LANCZOS)

            filename = f"{int(user_id)}_{uuid.uuid4().hex}.png"
            path = PROFILE_DIR / filename
            image.save(path, "PNG", optimize=True)
    except Exception:
        return False, "File bukan gambar yang valid atau rusak.", None

    try:
        with get_connection() as conn:
            old_row = conn.execute(
                "SELECT profile_photo_path FROM users WHERE id = ?;", (int(user_id),)
            ).fetchone()
            old_path = Path(old_row["profile_photo_path"]) if old_row and old_row["profile_photo_path"] else None
            conn.execute(
                "UPDATE users SET profile_photo_path = ? WHERE id = ?;",
                (str(path), int(user_id)),
            )
            conn.commit()
        if old_path and old_path != path and old_path.parent == PROFILE_DIR:
            old_path.unlink(missing_ok=True)
    except Exception:
        try:
            path.unlink(missing_ok=True)
        except Exception:
            pass
        return False, "Foto profil gagal disimpan.", None

    return True, "Foto profil berhasil diperbarui.", path


def remove_profile_photo(user_id: int) -> tuple[bool, str]:
    path = get_profile_photo_path(user_id)
    try:
        with get_connection() as conn:
            conn.execute(
                "UPDATE users SET profile_photo_path = NULL WHERE id = ?;",
                (int(user_id),),
            )
            conn.commit()
        if path and path.parent == PROFILE_DIR:
            path.unlink(missing_ok=True)
        return True, "Foto profil berhasil dihapus."
    except Exception:
        return False, "Foto profil gagal dihapus."
