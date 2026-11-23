"""BIOVA Mascot & Missing Asset Placeholder Component
Provides a reusable placeholder for missing visual assets (mascot, 3D models, etc.).
All mascot image usage has been replaced with this placeholder per design revision.
"""

import streamlit as st
from components.icons import render_icon
from services.config import COLOR_BORDER, COLOR_CARD, COLOR_TEXT


def missing_asset_placeholder(
    label: str = "Aset belum tersedia",
    width: int = 180,
    height: int = 140,
    center: bool = True,
):
    """Renders a dashed-border placeholder box for any missing visual asset.

    Args:
        label: Context text shown below the X mark (e.g. "Maskot", "Model 3D").
        width: Width of the placeholder box in pixels.
        height: Height of the placeholder box in pixels.
        center: Whether to horizontally center the box.
    """
    align = "margin: 12px auto 14px auto;" if center else "margin: 12px 0 14px 0;"
    html = f"""
    <div style="
        width: {width}px;
        max-width: 100%;
        height: {height}px;
        border: 2.5px dashed {COLOR_BORDER};
        border-radius: 16px;
        background-color: {COLOR_CARD};
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        {align}
    ">
        <div style="margin-bottom:6px;">
            {render_icon("info", 36, "biova-icon--heading", label)}
        </div>
        <div style="
            font-size: 11px;
            color: #888888;
            font-weight: 600;
            text-align: center;
            padding: 0 10px;
        ">{label}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_mascot(mood: str = "happy", width: int = 140, center: bool = True):
    """Legacy API — now delegates to the placeholder.
    Kept for backward compatibility so existing imports don't break.
    """
    mood_labels = {
        "happy": "Maskot (senang)",
        "success": "Maskot (berhasil)",
        "sad": "Maskot (sedih)",
        "celebrate": "Maskot (selebrasi)",
        "welcome": "Maskot halaman utama",
    }
    label = mood_labels.get(mood, "Maskot belum tersedia")
    # Map width to reasonable placeholder sizes
    ph_w = min(width, 200)
    ph_h = int(ph_w * 0.72)
    missing_asset_placeholder(label=label, width=ph_w, height=ph_h, center=center)
