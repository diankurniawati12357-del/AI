"""BIOVA Reusable UI Cards
Card templates for Dashboard categories, Panorama banner, and content presentations.
"""

import streamlit as st
from services.config import (
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_CARD,
    COLOR_BORDER,
    COLOR_HIGHLIGHT,
    COLOR_TEXT,
)


def render_category_card(
    category_id: str,
    title: str,
    icon: str,
    description: str,
    on_click_callback=None,
):
    """Renders category selection card (Hewan or Tumbuhan) matching the UI screenshot."""
    st.markdown(
        f"""
        <div class="biova-card">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                <div style="font-size: 28px; width: 44px; height: 44px; border-radius: 12px; background-color: {COLOR_HIGHLIGHT}; display: flex; align-items: center; justify-content: center;">
                    {icon}
                </div>
                <div>
                    <h3 style="margin: 0; font-size: 19px; font-weight: 800; color: {COLOR_PRIMARY};">{title}</h3>
                </div>
            </div>
            <p style="font-size: 13px; color: #444444; margin-bottom: 12px; line-height: 1.4;">
                {description}
            </p>
            <div style="font-size: 11px; color: #777777; margin-bottom: 8px;">
                Format yang didukung: JPG, JPEG, PNG
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(f"Unggah Gambar {title}", key=f"btn_upload_{category_id}", use_container_width=True):
        if on_click_callback:
            on_click_callback(category_id)


def render_panorama_banner(on_click_callback=None):
    """Renders the dark green Panorama card on the Dashboard."""
    st.markdown(
        f"""
        <div class="biova-card-highlight">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="font-size: 26px; width: 44px; height: 44px; border-radius: 12px; background-color: rgba(255, 255, 255, 0.15); display: flex; align-items: center; justify-content: center;">
                        🌄
                    </div>
                    <div>
                        <h4 style="margin: 0; font-size: 17px; font-weight: 800;">Buat Panorama dari Fotomu!</h4>
                        <p style="margin: 2px 0 0 0; font-size: 12px; opacity: 0.9;">Gabungkan beberapa foto menjadi satu pemandangan indah.</p>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Mulai Buat Panorama →", key="btn_dash_panorama", use_container_width=True):
        if on_click_callback:
            on_click_callback()
