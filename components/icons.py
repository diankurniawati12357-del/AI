"""Centralized access to BIOVA's bundled transparent PNG icons."""

import base64
import html
from functools import lru_cache
from pathlib import Path

import streamlit as st
import logging


_ICON_DIR = Path(__file__).resolve().parent.parent / "icon"
_LOGGER = logging.getLogger("biova.icons")

ANIMAL_ICONS = {
    "mamalia": "icon_mamalia.png",
    "aves": "icon_aves.png",
    "reptilia": "icon_reptilia.png",
    "amfibi": "icon_amfibi.png",
    "pisces": "icon_pisces.png",
    "invertebrata": "icon_invertebrata.png",
}

ANIMAL_CLASS_ICONS = ANIMAL_ICONS

ANIMAL_CLASS_ICONS = {
    "mamalia": "icon_mamalia.png",
    "aves": "icon_aves.png",
    "reptilia": "icon_reptilia.png",
    "reptil": "icon_reptilia.png",
    "amfibi": "icon_amfibi.png",
    "pisces": "icon_pisces.png",
    "invertebrata": "icon_invertebrata.png",
}


def normalize_animal_class(class_name: str) -> str:
    """Normalize presentation-only animal class names without changing model labels."""
    normalized = (class_name or "").strip().lower()
    normalized = normalized.replace("kelas:", "").replace("class:", "").strip()
    normalized = normalized.split("(")[0].strip()
    for alias in ("reptilia", "reptil", "mamalia", "aves", "amfibi", "pisces", "invertebrata"):
        if normalized.startswith(alias):
            return alias
    return normalized


def get_animal_class_icon(class_name: str):
    """Return the bundled icon name and normalized class for a UI animal class."""
    normalized = normalize_animal_class(class_name)
    icon_name = ANIMAL_CLASS_ICONS.get(normalized)
    if icon_name:
        return icon_name, normalized
    if normalized:
        _LOGGER.warning("Animal icon class not recognized: %s", class_name)
    return "icon_pengguna.png" if (_ICON_DIR / "icon_pengguna.png").is_file() else "tumbuhan", normalized


PLANT_TOPIC_ICONS = {
    "biji_keping": "icon_bijikeping.png",
    "sistem_perakaran": "icon_sistemperakaran.png",
    "tulang_daun": "icon_strukturtulangdaun.png",
    "batang_kambium": "icon_batangkambium.png",
    "struktur_bunga": "icon_strukturbunga.png",
    "biji": "icon_bijikeping.png",
    "keping": "icon_bijikeping.png",
    "akar": "icon_sistemperakaran.png",
    "perakaran": "icon_sistemperakaran.png",
    "daun": "icon_strukturtulangdaun.png",
    "tulang": "icon_strukturtulangdaun.png",
    "batang": "icon_batangkambium.png",
    "kambium": "icon_batangkambium.png",
    "bunga": "icon_strukturbunga.png",
}


def get_plant_topic_icon(topic_name: str) -> str:
    normalized = (topic_name or "").strip().lower()
    normalized = normalized.replace("-", "_").replace(" ", "_")
    if normalized in PLANT_TOPIC_ICONS:
        return PLANT_TOPIC_ICONS[normalized]
    for key, icon_name in PLANT_TOPIC_ICONS.items():
        if key in normalized:
            return icon_name
    return "tumbuhan"


@lru_cache(maxsize=64)
def _resolve_icon(filename: str):
    path = (_ICON_DIR / filename).resolve()
    if path.parent != _ICON_DIR.resolve() or not path.is_file():
        return None
    return path


def _filename(name: str) -> str:
    filename = name if name.lower().endswith(".png") else f"icon_{name}.png"
    return Path(filename).name


def get_icon_path(name: str):
    """Return the absolute path for a bundled icon, or None when unavailable."""
    return _resolve_icon(_filename(name))


@lru_cache(maxsize=64)
def _read_icon_data(filename: str):
    path = get_icon_path(filename)
    if path is None:
        return None
    return base64.b64encode(path.read_bytes()).decode("ascii")


def get_icon_base64(name: str):
    """Return a cached base64-encoded PNG, or None when the icon is missing."""
    return _read_icon_data(_filename(name))


def render_icon(
    name: str,
    size: int = 24,
    css_class: str = "",
    alt: str = "",
    *,
    as_html: bool = True,
):
    """Render a bundled icon as HTML or with Streamlit's native image renderer.

    HTML mode returns an <img> tag using an embedded data URI. Streamlit mode
    displays the local asset directly. Missing files render an accessible,
    non-broken fallback instead of a broken image.
    """
    size = max(1, int(size))
    classes = " ".join(
        part for part in ("biova-icon", css_class.strip()) if part
    )
    safe_classes = html.escape(classes, quote=True)
    safe_alt = html.escape(alt or name.replace("_", " "), quote=True)
    path = get_icon_path(name)

    if as_html:
        if path is None:
            return (
                f'<span class="biova-icon-fallback {safe_classes}" role="img" '
                f'aria-label="{safe_alt}" style="width:{size}px;height:{size}px">'
                f"{html.escape((alt or name)[:1])}</span>"
            )
        data = get_icon_base64(name)
        if data is None:
            return (
                f'<span class="biova-icon-fallback {safe_classes}" role="img" '
                f'aria-label="{safe_alt}" style="width:{size}px;height:{size}px">'
                f"{html.escape((alt or name)[:1])}</span>"
            )
        return (
            f'<img class="{safe_classes}" src="data:image/png;base64,{data}" '
            f'alt="{safe_alt}" width="{size}" height="{size}" '
            'style="object-fit:contain;vertical-align:middle" />'
        )

    if path is None:
        st.markdown(render_icon(name, size, css_class, alt, as_html=True), unsafe_allow_html=True)
    else:
        st.image(str(path), width=size, caption=alt or None)
    return None
